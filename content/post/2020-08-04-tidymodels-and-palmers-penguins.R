## ----self_running, eval=FALSE, include = FALSE--------------------------------
## knitr::purl("./2020-08-04-tidymodels-and-palmers-penguins.Rmd")
## source("./2020-08-04-tidymodels-and-palmers-penguins.R")


## ----packages-----------------------------------------------------------------
pacman::p_load(magrittr,
               tidyverse,
               ggplot2,
               tidymodels
               )



## ----prepping_data------------------------------------------------------------
penguins     <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-07-28/penguins.csv')

penguins %>% dim
summary(penguins)

penguins %>%
    skimr::skim()



## ----cleaning_data------------------------------------------------------------
penguins$species <- penguins$species %>%
    as.factor()
penguins <- penguins[-(penguins$bill_length_mm %>% is.na() %>% which()),]



## ----met_vs_spc, fig.align = "center", fig.cap = "metrics vs species"---------
penguins.pivot <- penguins %>%
    pivot_longer(cols = bill_length_mm:body_mass_g,
                 names_to = "metrics",
                 values_to = "values")

penguins.pivot %>%
    ggplot(aes(values, fill = species)) +
    geom_histogram(bins = 20) +
    facet_wrap(~ metrics, scales = "free_x")



## ----data_splitting-----------------------------------------------------------
penguins.split <- penguins %>%
    rsample::initial_split(prop = 0.65, strata = species)

penguins.train <- penguins.split %>%
    rsample::training()

penguins.test <- penguins.split %>%
    rsample::testing()

penguins.cv <- penguins.train %>%
    rsample::vfold_cv(v = 10)



## ----model_making-------------------------------------------------------------
model.fit.prep <- parsnip::rand_forest(mode = "classification") %>%
    parsnip::set_engine("ranger") %>%
    tune::fit_resamples(species ~ bill_length_mm + bill_depth_mm + flipper_length_mm + body_mass_g,
                        resamples = penguins.cv)

model.fit.prep



## -----------------------------------------------------------------------------
model.fit <- parsnip::rand_forest(mode = "classification") %>%
    parsnip::set_engine("ranger") %>%
    fit(species ~ bill_length_mm + bill_depth_mm + flipper_length_mm + body_mass_g,
                        data = penguins.train)

model.fit



## ----metrics_study------------------------------------------------------------
penguins.fit.pred <- model.fit %>%
    predict(penguins.test) %>%
    bind_cols(penguins.test)



## ----metrics_study_2----------------------------------------------------------
penguins.fit.pred %>%
    metrics(species, estimate = .pred_class)



## ----curves_study, fig.align = "center", fig.cap = "ROC"----------------------
penguins.met <- model.fit.prep %>%
    predict(penguins.test, type = "prob") %>%
    bind_cols(penguins.test) %>%
    yardstick::gain_curve(species,
                          .pred_Adelie,
                          .pred_Chinstrap,
                          .pred_Gentoo)

penguins.met %>%
    autoplot() +
    ggpubr::theme_pubclean() +
    theme(strip.background = element_blank())


