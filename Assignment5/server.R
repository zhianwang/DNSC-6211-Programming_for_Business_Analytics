#Programming Assignment5
#Group3
#Shiny

library(shiny)
library(ggplot2)
function(input, output,session) {
  
#Selecting variables from the input file and mapping them to the selection drop down 1
  output$xvariable = renderUI({
    infile <- input$file1
    if (is.null(infile))
      return(selectInput('xcol', 'X Variables', ' '))
    
    selectedData = read.csv(infile$datapath)
    selectInput('xcol', 'X Variables', names(selectedData),
                selected=names(selectedData)[1])
  })
  
#Selecting variables from the input file and mapping them to the selection drop down 2
  output$yvariable = renderUI({
    infile <- input$file1
    if (is.null(infile))
      return(selectInput('ycol', 'Y Variables', ' '))
    
    selectedData = read.csv(infile$datapath)
    selectInput('ycol', 'Y Variables', names(selectedData),
                selected=names(selectedData)[2])
  })
  
#Plotting the graphs
  output$plot1 <- renderPlot({
    infile<-input$file1
    if (is.null(infile))
      return(NULL)
    df=read.csv(infile$datapath)
    selectedData=df[,c(input$xcol,input$ycol)]
    
    #Plotting the scatter plot of the 2 variables selected
    if(is.null(input$checkGroup)){
      o<-ggplot(data=selectedData[, c(input$xcol,input$ycol)],aes_string(x =input$xcol,y =input$ycol))+
        geom_point(color='steelblue',size=4)
      print(o)
    }
    
    #plotting Linear regression along with scatter plot
    else if(input$checkGroup[1]==1 && is.na(input$checkGroup[2])){
      p<-ggplot(data=selectedData[, c(input$xcol, input$ycol)],aes_string(x =input$xcol,y =input$ycol))+
        geom_point(color='steelblue',size=4)+
        geom_smooth(method='lm',se=FALSE,color='red',size=input$thicknesSlider)
      print(p)
    }
    
    #plotting the Quadratic regression along with scatter plot
    else if(input$checkGroup[1]==2 && is.na(input$checkGroup[2])){
      q<-ggplot(data=selectedData[, c(input$xcol, input$ycol)],aes_string(x =input$xcol,y =input$ycol))+
        geom_point(color='steelblue',size=4)+
        stat_smooth(method="lm", formula = y~poly(x,2),se=FALSE,color='green',size=input$thicknesSlider)
      print(q)
    }
    
    #Plotting both Linear and Quadratic regression along with scatter plot
    else if(input$checkGroup[1]==1 && input$checkGroup[2]==2){
      r<-ggplot(data=selectedData[, c(input$xcol, input$ycol)],aes_string(x =input$xcol,y =input$ycol))+
        geom_point(color='steelblue',size=4)+
        geom_smooth(method='lm',se=FALSE,color='red',size=input$thicknesSlider)+
        stat_smooth(method="lm", formula = y~poly(x,2),se=FALSE,color='green',size=input$thicknesSlider)
      print(r)
    }
    
    
  })
  
}

