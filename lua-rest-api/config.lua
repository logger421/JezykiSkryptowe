local config = require("lapis.config")

config("development", {
  server = "nginx",
  code_cache = "off",
  num_workers = "1",
  mysql = {
    host = "127.0.0.1",
    user = "db-user",
    password = "FILL_ME",
    database = "FILL_ME"
  }
})
