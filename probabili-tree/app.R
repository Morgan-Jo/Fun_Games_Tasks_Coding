# app.R
library(shiny)
library(ggplot2)
library(shinythemes)

# Load the statistical engine
source("scr-R/game_logic.R")

# --- UI Definition ---
ui <- fluidPage(
  theme = shinytheme("superhero"), # A dark, "terminal" style theme
  titlePanel("🌲 Probabili-Tree: The Survival Statistician"),
  
  sidebarLayout(
    sidebarPanel(
      h4("Survival Dashboard"),
      hr(),
      # Display game stats in a clean list
      uiOutput("stats_display"),
      hr(),
      
      p("Decide your fate based on the distribution:"),
      actionButton("forage", "Forage for Food", class = "btn-success btn-block"),
      br(),
      actionButton("rest", "Rest (Skip Day)", class = "btn-warning btn-block"),
      
      hr(),
      tags$b("Log:"),
      textOutput("game_log")
    ),
    
    mainPanel(
      # Visualizing the risk
      plotOutput("risk_plot", height = "400px"),
      br(),
      wellPanel(
        h4("Analyst's Note:"),
        textOutput("analyst_advice")
      )
    )
  )
)

# --- Server Logic ---
server <- function(input, output, session) {
  
  # Initialize Reactive Game State
  state <- reactiveValues(
    day = 1,
    health = 100,
    inventory = 0,
    risk_data = generate_risk_dist(1),
    message = "Analyze the variance. If the 'Danger Zone' is crowded, do not forage!",
    game_over = FALSE
  )
  
  # 1. Render the Risk Distribution Plot
  output$risk_plot <- renderPlot({
    df <- data.frame(val = state$risk_data)
    
    ggplot(df, aes(x = val)) +
      geom_histogram(fill = "#3498db", color = "white", bins = 25) +
      geom_vline(xintercept = 2.0, linetype = "dashed", color = "#e74c3c", size = 1.5) +
      annotate("text", x = 2.5, y = 5, label = "DEADLY RISK", color = "#e74c3c", fontface = "bold") +
      labs(title = paste("Day", state$day, "Environmental Survey"),
           x = "Standard Deviations of Risk", y = "Sensor Frequency") +
      theme_minimal()
  })
  
  # 2. Handle Foraging Action
  observeEvent(input$forage, {
    if(state$game_over) return()
    
    result <- process_turn(state$risk_data, "forage")
    
    if (!result$survived) {
      state$health <- 0
      state$message <- result$msg
      state$game_over <- TRUE
    } else {
      state$inventory <- state$inventory + 1
      state$day <- state$day + 1
      state$message <- result$msg
      state$risk_data <- generate_risk_dist(state$day) # Get new data for next day
    }
  })
  
  # 3. Handle Resting Action
  observeEvent(input$rest, {
    if(state$game_over) return()
    
    state$day <- state$day + 1
    state$message <- "You played it safe. The environment has shifted."
    state$risk_data <- generate_risk_dist(state$day)
  })
  
  # 4. Text and UI Outputs
  output$stats_display <- renderUI({
    tagList(
      p(tags$b("Day: "), state$day, " "),
      p(tags$b("Health: "), state$health, "%"),
      p(tags$b("Supplies: "), state$inventory)
    )
  })
  
  output$game_log <- renderText({ state$message })
  
  output$analyst_advice <- renderText({
    safety_rating <- calculate_safety(state$risk_data)
    paste0("There is a ", round(safety_rating, 1), "% probability of survival if you forage now.")
  })
}

# Run the app
shinyApp(ui = ui, server = server)