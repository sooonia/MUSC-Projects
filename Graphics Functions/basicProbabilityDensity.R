#' @title Basic Probability Density Plot
#' @param preds vector of probabilities
#' @param cat vector or categories. Must be same length as preds
#' @param maxLevels maximum number of levels with cat to group by. Recommended <= 10. Default = 10
#' @param minFreq minimum number of observation within a given level in cat for the category to appear on the plot. Default = 1
#' @description a function for plotting the density of probabilities of an outcome with option for categorical grouping
#' @return a ggplot of the probability density
#' @export
#

basicProbDPlot <- function(preds, cat, maxLevels = 10, minFreq = 1){
  
  mydata = as.data.frame(preds)
  colnames(mydata) <- 'preds'
  mydata$cat <- cat
  
  if(missing(cat)){
    
    ggplot(mydata, aes(preds)) +
      geom_density(fill = "palegreen2", colour = "black", alpha=.5) +
      ggtitle("Density of Predicted Probabilities") +
      labs(x="Predicted Probability",y="Density") +
      theme(plot.title = element_text(hjust = 0.5))
    
  }
  else{
    
    #Filter down to maxLevels
    if(length(levels(mydata$cat)) > maxLevels){
      tab <- table(mydata$cat)[order(table(mydata$cat),
                                     decreasing = TRUE)][1:maxLevels]
      names <- names(tab)
      mydata <- droplevels(mydata[mydata$cat %in% names,])
      print(paste("Filtered to top", maxLevels, "levels."))
      
    }
    #Remove levels below minFreq
    tab <- table(mydata$cat)[order(table(mydata$cat),
                                   decreasing = TRUE)]
    if(as.integer(tab[length(tab)]) < minFreq){
      tab <- tab[tab > minFreq]
      names <- names(tab)
      mydata <- droplevels(mydata[mydata$cat %in% names,])
      print(paste("Levels with fewer than", minFreq, "observations removed."))
    }
    
    if(length(tab) <= 10){
      ggplot(mydata, aes(x=preds, fill = cat)) +
        geom_density(alpha = .3) +
        ggtitle("Density of Predicted Probabilities by category") +
        labs(x="Predicted Probability",y="Density") +
        theme(plot.title = element_text(hjust = 0.5)) +
        guides(fill=guide_legend(title="Category")) +
        scale_fill_manual(values=c("dodgerblue4", "firebrick1", "forestgreen", "gold", "seashell", 
                                   "midnightblue", "lightblue1", "mediumorchid2", "lightseagreen", 
                                   "darkorange1"))}
    else{
      ggplot(mydata, aes(x=preds, fill = cat)) +
        geom_density(alpha = .3) +
        ggtitle("Density of Predicted Probabilities by category") +
        labs(x="Predicted Probability",y="Density") +
        theme(plot.title = element_text(hjust = 0.5)) +
        guides(fill=guide_legend(title="Category"))
    }
  }
  
}