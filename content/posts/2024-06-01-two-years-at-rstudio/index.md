---
title: Two years at RStudio
editor_options:
  chunk_output_type: console
execute:
  eval: false
---


``` r
library(ggplot2)
library(tidyverse)
library(lubridate)

files <- c(
  "data/machow+quartodoc/issue_comments.ndjson",
  "data/posit-dev+great-tables/issue_comments.ndjson"
)

issue_files <- c(
  "data/machow+quartodoc/issues.ndjson",
  "data/posit-dev+great-tables/issues.ndjson"  
)

stargazer_files <- c(
  "data/machow+quartodoc/stargazers.ndjson",
  "data/posit-dev+great-tables/stargazers.ndjson"  
  
)

# repos = tribble(
#   ~repository_id, ~repository_name,
#   "R_kgDOIX3w4Q", "machow/quartodoc",
#   "MDEwOlJlcG9zaXRvcnkxNjk4OTg1MzU=", "machow/siuba",
#   "R_kgDOHwCARA", "machow/siuba.org",
#   "R_kgDOGzb8NA", "rstudio/pins-python",
#   "R_kgDOG-6zQQ", "rstudio/pyshiny-site"
# )

comments_raw <- purrr::map(files, \(x) jsonlite::stream_in(file(x)))
comments <- tibble::tibble(data = comments_raw, repo = c("quartodoc", "great-tables")) |> tidyr::unnest(cols = c(data))
comments_enriched <- 
  comments %>%
  left_join(users %>% select(user_id = id, login), "user_id")



issues_raw <- purrr::map(issue_files, \(x) jsonlite::stream_in(file(x)))

issues <- tibble::tibble(data = issues_raw, repo = c("quartodoc", "great-tables")) |> tidyr::unnest(cols = c(data))

issues_enriched <- 
  issues %>%
  left_join(users %>% select(user_id = id, login), "user_id")

users_raw <- jsonlite::read_json("data/users.json")
users <- map_df(users, ~.)

stargazers_raw <- purrr::map(stargazer_files, \(x) jsonlite::stream_in(file(x)))
stargazers <- tibble::tibble(data = stargazers_raw, repo = c("quartodoc", "great-tables")) |> tidyr::unnest(cols = c(data)) %>% mutate(starred_at = as.POSIXct(starred_at,format = "%Y-%m-%dT%H:%M:%OSZ", tz = "UTC"))
```

``` r
events <- tibble(
  date = as.POSIXct(c("2023-12-21", "2024-04-04", "2023-04-01", "2024-07-01"))),
  event=c("PyCon Submission", "Top of Hackernews", "Goal: 6 users", "Goal: 12 users"),
  y = c(140, 400)
)



stargazers %>%
  arrange(repo, starred_at) %>%
  group_by(repo) %>%
  mutate(ttl = 1:n()) %>%
  ungroup() %>%
  filter(starred_at < "2024-04-06") %>%
  ggplot() +
  geom_line(aes(starred_at, ttl, color=repo)) +
  geom_point(aes(date, y), data = events) + 
  geom_label(aes(date - days(80), y, label=event), data=events) + 
  labs(title = "Total Github stars over time") + 
  scale_x_datetime(breaks = as.POSIXct(seq(ymd("2023-01-01"), ymd("2024-04-01"), by = "3 months"))) +
  coord_cartesian(xlim = c(as.POSIXct(date("2022-11-01")), NA)) 
```

``` r
comments_enriched %>%
  filter(created_at < "2024-04-01") %>%
  mutate(
    created_at = floor_date(date(created_at), "month"),
    login = fct_rev(fct_collapse(
      fct_infreq(login),
      machow = "machow",
      `rich-iannone`="rich-iannone",
      jrycw = "jrycw",      
      other_level = "Other"
    ))
    #login = fct_lump_n(login, 3)
  ) %>%
  ggplot(aes(created_at, fill=login)) +
  geom_bar() +
  facet_wrap(~repo, ncol=1) +
  scale_x_date(date_minor_breaks = "1 month", breaks = seq(ymd("2023-01-01"), ymd("2024-04-01"), by = "3 months"))
```

``` r
comments_enriched %>%
  filter(repo == "quartodoc") %>%
  mutate(
    created_at = floor_date(date(created_at), "month"),
    login = fct_lump(fct_rev(fct_infreq(login)), 5),
    login_friendly = fct_relabel(login, \(login) case_when(
      login == "pawamoy" ~ "pawamoy (griffe)",
      login == "wch" ~ "wch (shiny)",
      login == "has2k1" ~ "has2k1 (plotnine)",
      TRUE ~ login
    ))
  ) %>%
  ggplot(aes(created_at, fill=login)) +
  geom_bar() +
  facet_wrap(~login_friendly, ) +
  labs(title = "Issues comments over time on quartodoc")
```

``` r
comments_enriched %>%
  filter(repo == "quartodoc") %>% 
  mutate(is_michael = case_when(login == "machow" ~ "machow", TRUE ~ "other")) %>%
  mutate(
    created_at = floor_date(date(created_at), "month"),
    login = fct_lump_n(fct_rev(fct_infreq(login)), 7)
  ) %>%   
  ggplot(aes(created_at, fill=login)) + geom_bar() + facet_wrap(~is_michael, ncol=1)
```
