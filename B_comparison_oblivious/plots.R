  library(ggplot2)
  library(dplyr)
  library(matrixStats)
  
  make_plot <- function()
  {
    winexp_file_1   = './winexp_regrets0.00100.txt'
    exp3_file_1     = './exp3_regrets0.00100.txt'
    winexp_file_2   = './winexp_regrets0.01000.txt'
    exp3_file_2     = './exp3_regrets0.01000.txt'
    winexp_file_3   = './winexp_regrets0.10000.txt'
    exp3_file_3     = './exp3_regrets0.10000.txt'
    winexp_1        <- read.table(winexp_file_1,header=FALSE)
    exp3_1          <- read.table(exp3_file_1,header=FALSE)
    winexp_2        <- read.table(winexp_file_2,header=FALSE)
    exp3_2          <- read.table(exp3_file_2,header=FALSE)
    winexp_3        <- read.table(winexp_file_3,header=FALSE)
    exp3_3          <- read.table(exp3_file_3,header=FALSE)
    winexp_trans_1  <- t(winexp_1)
    exp3_trans_1    <- t(exp3_1)
    winexp_trans_2  <- t(winexp_2)
    exp3_trans_2    <- t(exp3_2)
    winexp_trans_3  <- t(winexp_3)
    exp3_trans_3    <- t(exp3_3)
    df_winexp_1       <- as.data.frame.matrix(winexp_trans_1)
    df_winexp_1$avg_regr = rowMeans(winexp_trans_1)
    df_winexp_1$y_low  = rowQuantiles(winexp_trans_1, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp_1$y_high = rowQuantiles(winexp_trans_1, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp_1$Algorithm = "WINEXP - 0.001"
    df_winexp_1$T = seq.int(nrow(df_winexp_1))
    df_winexp_2       <- as.data.frame.matrix(winexp_trans_2)
    df_winexp_2$avg_regr = rowMeans(winexp_trans_2)
    df_winexp_2$y_low  = rowQuantiles(winexp_trans_2, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp_2$y_high = rowQuantiles(winexp_trans_2, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp_2$Algorithm = "WINEXP - 0.01"
    df_winexp_2$T = seq.int(nrow(df_winexp_2))
    df_winexp_3       <- as.data.frame.matrix(winexp_trans_3)
    df_winexp_3$avg_regr = rowMeans(winexp_trans_3)
    df_winexp_3$y_low  = rowQuantiles(winexp_trans_3, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp_3$y_high = rowQuantiles(winexp_trans_3, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_winexp_3$Algorithm = "WINEXP - 0.1"
    df_winexp_3$T = seq.int(nrow(df_winexp_3))
    
    
    
    df_exp3_1       <- as.data.frame.matrix(exp3_trans_1)
    df_exp3_1$avg_regr = rowMeans(exp3_trans_1)
    df_exp3_1$y_low  = rowQuantiles(exp3_trans_1, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3_1$y_high = rowQuantiles(exp3_trans_1, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3_1$Algorithm   = "EXP3 - 0.001"
    df_exp3_1$T = seq.int(nrow(df_exp3_1))

    df_exp3_2 <- as.data.frame.matrix(exp3_trans_2)
    df_exp3_2$avg_regr      = rowMeans(exp3_trans_2)
    df_exp3_2$y_low     = rowQuantiles(exp3_trans_2, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3_2$y_high    = rowQuantiles(exp3_trans_2, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3_2$Algorithm   = "EXP3 - 0.01"
    df_exp3_2$T = seq.int(nrow(df_exp3_2))
    
    df_exp3_3       <- as.data.frame.matrix(exp3_trans_3)
    df_exp3_3$avg_regr   = rowMeans(exp3_trans_3)
    df_exp3_3$y_low  = rowQuantiles(exp3_trans_3, rows = NULL, cols = NULL, probs = c(0.1), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3_3$y_high = rowQuantiles(exp3_trans_3, rows = NULL, cols = NULL, probs = c(0.9), na.rm = FALSE, type = 7L, drop = TRUE)
    df_exp3_3$Algorithm   = "EXP3 - 0.1"
    df_exp3_3$T = seq.int(nrow(df_exp3_3))

    df_aggr_1 = rbind(df_exp3_1,df_winexp_1)
    df_aggr_2 = rbind(df_exp3_2,df_winexp_2)
    df_aggr_3 = rbind(df_exp3_3,df_winexp_3)
    

    df_aggr_4 = rbind(df_aggr_1, df_aggr_2)
    df_aggr   = rbind(df_aggr_4,df_aggr_3)

    rounds <- data.frame(0:4999)

    probs  <- c(0.1, 0.9) # the percentiles to be used

    step = seq(0,5000,by=2)
    rounds_step <- data.frame(1:500*100)
    
    ind = seq(1, 30000, 100)
    ind2 = seq(1, 30000, 500)
    
    df_step = df_aggr[ind,]
    #print (typeof(df_step))
    df_step2 = df_aggr[ind2,]
   

    ggplot(df_step) +
      geom_ribbon(aes(x = T, ymin = y_low, ymax = y_high, fill=Algorithm), alpha=0.1) + guides(fill=FALSE) +
      #geom_errorbar(aes(x = c_s, ymin = y_low, ymax = y_high), width=0.05, color = 'black', size = 0.1) +
      geom_line(aes(x=T, y=avg_regr, color = Algorithm, linetype = Algorithm), size = 1) +
      geom_point(data=df_step2, aes(x=T, y=avg_regr, color = Algorithm, shape=Algorithm), size = 3) +
      #scale_x_continuous(breaks = seq(0, 5000, 100))+
      scale_y_continuous(
        breaks = c(0,10,20,30,40,50,60,70,80,90,100)
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
      
	  ggsave('./b_comparison_oblivious.png')

  }
  
  
  make_plot()
