build_model <- function(rd, predVars, splitDate, clusterSize = 2){
  td<-rd
  ##drops patients that have cancled or already arrived
  td.s<-droplevels(td[td$ApptStatus == 'Completed' | 
                        td$ApptStatus == 'No Show',])
  td.s$APPTWeekday<-as.factor(td.s$APPTWeekday)
  td.s$APPTWeekday<-as.factor(td.s$APPTHour)
  targetCol = 'ApptStatus'
  outcome = 'No Show'
  
  ## split data into train and test sets at 3rd quartile date            
  train_data<- td.s[td.s$APPTDATE <= splitDate, ]
  eval_data<-td.s[td.s$APPTDATE > splitDate, ]
  
  ## learn catagorical encoing transform
  library(doParallel)
  library(parallel)
  ## start parallel cluster
  print("Building Treatments")
  cl<-makeCluster(clusterSize)
  treatment<-designTreatmentsC(train_data, 
                               varlist = predVars,
                               outcomename = targetCol,
                               outcometarget = outcome,
                               rareCount = 20,
                               parallelCluster = cl)
  stopCluster(cl)
  print("Completed Building Treatments")
  
  ## apply variable encoding to training and eval sets
  train_data.t<-prepare(treatment, train_data, pruneSig = .001)
  eval_data.t<-prepare(treatment, eval_data, pruneSig = .001)
  
  ## create preProc to range and near zero var
  preProc<-preProcess(train_data.t, method = c('range', 'nzv', 'zv'))
  
  ## apply pre proc to training and eval sets
  train_data.tp<-predict(preProc, train_data.t)
  eval_data.tp<-predict(preProc, eval_data.t)
  
  ## downSample trainData to balance the classes 
  train_data.tp.ds<-downSample(x = train_data.tp[, !colnames(train_data.tp) %in% targetCol],
                               y = train_data.tp[,targetCol],
                               yname = targetCol)
  
  ## get the list of predictors
  measures<-colnames(train_data.tp.ds)[!colnames(train_data.tp.ds) %in% targetCol]
  
  ##set up the training and test sets for mxnet
  xTrain <- as.matrix(train_data.tp.ds[, measures])
  yTrain <- ifelse(train_data.tp.ds[, targetCol] == outcome, 1,0)
  xTest <- as.matrix(eval_data.tp[, measures])
  yTest <-ifelse(eval_data.tp[,targetCol] == outcome,1,0)
  eval.data = list(data = xTest, label = yTest )
  
  ## setup array iterators
  trainIterator <-mx.io.arrayiter(data = t(xTrain), 
                                  label = yTrain, 
                                  batch.size = 500, 
                                  shuffle = TRUE)
  
  evalIterator <-mx.io.arrayiter(data = t(xTest), 
                                 label = yTest, 
                                 batch.size = 500, 
                                 shuffle = FALSE)
  
  ##Define the network
  data <- mx.symbol.Variable("data")
  fc1 <- mx.symbol.FullyConnected(data, name="fc1", num_hidden=200)
  act1 <- mx.symbol.Activation(fc1, name="relu1", act_type="relu")
  drop1<-mx.symbol.Dropout(act1, p = .2, name = 'drop1')
  
  fc2 <- mx.symbol.FullyConnected(drop1, name="fc2", num_hidden=200)
  act2 <- mx.symbol.Activation(fc2, name="relu2", act_type="relu")
  drop2<-mx.symbol.Dropout(act2, p = .2, name = 'drop1')
  
  fc3 <- mx.symbol.FullyConnected(drop2, name="fc3", num_hidden=2)
  softmax <- mx.symbol.SoftmaxOutput(fc3, name="sm")
  
  ##creates a logloss metric for evaluation
  mx.metric.mlogloss <- mx.metric.custom("mlogloss", function(label, pred){
    
    label <- as.factor(label)
    label_mat <- matrix(0, nrow = length(label), ncol = length(levels(label)))
    sample_levels <- as.integer(label)
    for (i in 1:length(label)) label_mat[i, sample_levels[i]] <- 1
    label <- label_mat
    
    label <- as.vector(t(label))
    eps <- 1e-15
    n <- nrow(pred)
    pred <- pmax(pmin(pred, 1 - eps), eps)
    MultiLogLoss <- (-1/n) * sum(label * log(pred))
    return(MultiLogLoss)
  })
  
  ## set up mxnet trainiing
  #devices = mx.gpu()
  a<-Sys.time()
  mx.set.seed(0)
  ##train Model 
  
  model <- mx.model.FeedForward.create(softmax, 
                                       X = trainIterator,
                                       #ctx=devices, 
                                       num.round=20,
                                       learning.rate=.005, momentum=0.95,
                                       eval.data = evalIterator,
                                       eval.metric=mx.metric.accuracy,
                                       initializer=mx.init.uniform(0.1)#,
                                       #epoch.end.callback = mx.callback.save.checkpoint("model/patientSlotNet")
                                       #,arg.params = checkPointModel$arg.params
  )
  b<-Sys.time()-a
  print(paste("Model Build Time: ",b))
  
  obs<- as.factor(eval_data[,targetCol])
  preds<-predict(model,as.matrix(eval_data.tp[, measures]), 
                 array.layout =   "rowmajor")
  preds<-data.frame(preds[1,], preds[2,])
  colnames(preds)<-levels(obs)
  
  ## plot performance vs cutoff for test set 
  pref<-prediction(predictions = preds[,2], labels = obs)
  plot(performance(pref, 'acc',x.measure = 'cutoff' ))
  
  
  
  ## set thge cutoff 
  cutoff<-.75
  newPreds<-as.factor(ifelse( preds[,2]> cutoff ,1,0))
  levels(newPreds)<-levels(obs)
  ## get the confusion matrix
  caret::confusionMatrix(data = newPreds, 
                         reference = obs)
  ## get two class summary 
  twoClassSummary(data = data.frame(obs = obs,pred = newPreds, preds  ) ,
                  lev = levels(obs), 
                  model = 'mxnet' )
  
  
  ## test Preformanc against training Set 
  predsp<-predict(model,as.matrix(train_data.tp[, measures]), 
                  array.layout =   "rowmajor")[2,]
  predsr<-as.factor(ifelse(predsp > .5,1,0))
  obs<- as.factor(train_data[,targetCol])
  ## get the ROC 
  r<-pROC::roc(obs, predsp)
  print(r)
  ## get the confusion matrix
  preds<-predsr
  levels(preds)<-levels(obs)
  caret::confusionMatrix(data = preds, 
                         reference = obs)
  
  return(model)
  
}