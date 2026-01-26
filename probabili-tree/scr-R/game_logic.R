# game_logic.R
# This script handles the statistical simulations and state transitions

#' Generate Environmental Risk Data
#' @description Creates a distribution of risk factors based on current difficulty
#' @param level Integer representing the current game day/difficulty
#' @return A numeric vector representing the risk distribution
generate_risk_dist <- function(level) {
  # As the level increases, the variance (SD) and mean risk creep up
  base_mean <- -0.5 + (level * 0.1)
  base_sd <- 0.5 + (level * 0.05)
  
  # Generate a mixture of normal and some random noise (Black Swan potential)
  dist <- rnorm(100, mean = base_mean, sd = base_sd)
  return(dist)
}

#' Calculate Survival Probability
#' @description Helper to determine the mathematical 'safety' of a forage action
#' @param dist The current risk distribution vector
#' @param threshold The death threshold (default is 2.0)
calculate_safety <- function(dist, threshold = 2.0) {
  prob_safe <- sum(dist < threshold) / length(dist)
  return(prob_safe * 100)
}

#' Process Turn Outcome
#' @description Determines if the player survives the foraging attempt
#' @param dist The current risk distribution
#' @param action String "forage" or "rest"
#' @return List containing survival status and a message
process_turn <- function(dist, action) {
  if (action == "rest") {
    return(list(survived = TRUE, msg = "You rested and stayed safe, but your hunger grows."))
  }
  
  # The "Gamble": Randomly sample one data point from the distribution
  outcome <- sample(dist, 1)
  
  if (outcome >= 2.0) {
    return(list(survived = FALSE, 
                msg = paste("Critical Failure! You hit a risk event of", round(outcome, 2))))
  } else {
    return(list(survived = TRUE, 
                msg = paste("Success! You navigated a risk of", round(outcome, 2))))
  }
}