  library(ggplot2)
  library(dplyr)
  library(matrixStats)
  
  make_plot <- function()
  {
    winexp_file = './winexp_regrets.txt'
    exp3_file     = './exp3_regrets.txt'
    winexp        <- read.table(winexp_file,header=FALSE)
    exp3          <- read.table(exp3_file,header=FALSE)
    winexp_trans  <- t(winexp)
    exp3_trans    <- t(exp3)
    df_winexp      <- as.data.frame.matrix(winexp_trans)
    df_winexp$avg_regr = rowMeans(winexp_trans)
    df_winexp$y_low  = rowQuantiles(winexp_trans, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp$y_high = rowQuantiles(winexp_trans, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp$Algorithm = "1. WINEXP"
    df_exp3       <- as.data.frame.matrix(exp3_trans)
    df_exp3$avg_regr = rowMeans(exp3_trans)
    df_exp3$y_low  = rowQuantiles(exp3_trans, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3$y_high = rowQuantiles(exp3_trans, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3$Algorithm   = "2. EXP3"

    

    df_aggr = rbind(df_exp3,df_winexp)
    rounds <- data.frame(1:5000)

    probs  <- c(0.1, 0.9) # the percentiles to be used

    
    
    ggplot(df_aggr) +
      geom_ribbon(aes(x = rounds, ymin = y_low, ymax = y_high, fill=Algorithm), alpha=0.3) + guides(fill=FALSE) +
      geom_line(aes(x=rounds, y=avg_regr, color = Algorithm, linetype = Algorithm), size = 1) +
      scale_y_continuous(
        breaks = c(0,10,20,30,40,50,60)
      )+
      theme_bw() +
      theme(
	  plot.title = element_text(hjust = 0.5, face = 'bold', size = 24),
        axis.title.x = element_text(size = 20),
        axis.title.y = element_text(size = 20),
        axis.text.x = element_text(size = 20),
        axis.text.y = element_text(size = 20),
        legend.key.height = unit(c(1), "cm"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.position = c(0.01,0.99), 
        legend.title=element_text(size=20),
        legend.text = element_text(size=20),
        legend.justification = c(0, 1),
        legend.key.width = unit(1, "cm")
      ) +
      xlim(0,5000)+
      xlab('number of rounds') +
      ylab('regret') 
      
	  ggsave('./exp3_adv_noisy_1000.png')

  }
  
  
  make_plot()
