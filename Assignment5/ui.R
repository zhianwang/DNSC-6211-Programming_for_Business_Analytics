#Programming Assignment5
#Group3
#Shiny

library("shiny")
fluidPage( 
  #sidebar layout gives the layout of the output needed   
   sidebarLayout(
  #sidebar panel provides the output panel with required options
      sidebarPanel(
        #implements the file input box 
        fileInput('file1', label = h3("File input"),
                  accept=c('text/csv','text/comma-separated-values,text/plain','.csv')),
        #Implements the column selection
        uiOutput('xvariable'),
        uiOutput('yvariable'),
        #Implements the checkbox functionality
        checkboxGroupInput("checkGroup",label=h3("Checkbox Group"),
        choices=list("Linear Model"=1,"Quadratic Model"=2),selected=0),
        #implements the slider functionality
        sliderInput("thicknesSlider",label=h3("Line Thickness"),min=1,max=5,value=1)
        
  ),
  mainPanel(
    #plots the graphs
    plotOutput('plot1')
        )
  
     )
)


