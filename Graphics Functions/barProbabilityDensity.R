#' @title Bar Probability Density Plot
#' @param preds vector of probabilities
#' @param class vector containing actual classifications
#' @param numBins Number of bins to form from probabilities. Default is 10
#' @description a function for plotting the density of probabilities of an outcome with grouped bars of actual classifications underneath
#' @return a ggplot of the probability density with grouped bars of actual classifications underneath
#' @export
#
barProbDPlot <- function(preds, class, numBins = 10){
  
  mydata = as.data.frame(preds)
  colnames(mydata) <- 'preds'
  mydata$actualClass <- class
  
  if(length(levels(mydata$actualClass))>10){
    tab <- table(mydata$actualClass)[order(table(mydata$actualClass),
                                           decreasing = TRUE)][1:10]
    names <- names(tab)
    print("Warning: Number of classes exceeds 10. Only using data in the following classes:")
    mydata <- mydata[mydata$actualClass %in% names,]
    print(names)
  }
  
  binw <- 1/(numBins-1)
  
  scale <- max(ggplot_build(ggplot(mydata, aes(preds)) +
                              geom_histogram(aes(fill=actualClass), 
                                             binwidth = binw, 
                                             col="black", 
                                             size=.1))$data[[1]]$ymax)*.55
  eval(substitute(
    expr = {
      ggplot(mydata, aes(preds)) +
        geom_histogram(aes(fill=actualClass), 
                       binwidth = binw, 
                       col="black", 
                       size=.1)+
        geom_density(aes(y=(..density..*scale)), fill = "seashell", alpha=.1)+
        ggtitle("Counts of Classes by Predicted Probability") +
        labs(x="Predicted Probability",y="Count") +
        theme(plot.title = element_text(hjust = 0.5))+
        guides(fill=guide_legend(title="Class"))+
        scale_fill_manual(values=c("dodgerblue4", "firebrick3", "forestgreen","darkorange1", "seashell", 
                                   "midnightblue", "lightblue1", "mediumorchid2", "lightseagreen", "gold"))
      
    }, 
    env = list(scale=scale)))
  
  
}
