local lapis = require("lapis")
local Model = require("lapis.db.model").Model

local app = lapis.Application()

local Products = Model:extend("products", {
  primary_key = "id"
})

local Categories = Model:extend("categories", {
  primary_key = "id",
  relations = {
    { "products", has_many = "Products" }
  }
})

app:get("/", function(self)
  return "Welcome to Lapis "..require("lapis.version").." based shop"
end)

-- Get all categories
app:get("/categories", function(self)
  self.json = Categories:select()
  return { json = self.json }
end)

-- Get all products
app:get("/products", function(self)
  self.json = Products:select()
  return { json = self.json }
end)

app:match("/categories/:category", function(self)
  local categoryDAO = Categories:find({ name = self.params.category})
  self.json = categoryDAO:get_products()
  return { json = self.json }
end)

return app
