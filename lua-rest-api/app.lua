local lapis = require("lapis")
local Model = require("lapis.db.model").Model
local json_params = require("lapis.application").json_params

local app = lapis.Application()

local Products = Model:extend("products", {
  primary_key = "id"
})

local Categories = Model:extend("categories", {
  primary_key = "id"
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
  return { json = { success = true, product = self.json } }
end)

-- Get product by id
app:get("/products/:id", function (self)
  self.json = Products:find(self.params.id)
  return { json = { success = true, product = self.json } }
end)

-- Get products by category they belong (named)
app:get("/products/:category", function(self)
  local categoryDAO = Categories:find({ name = self.params.category })
  if not categoryDAO then
    return { json = { success = false, message = "No such category, products can't be listed!" }}
  else 
    self.json = Products:select("where category_id = ?", categoryDAO["id"])
    return { json = { success = true, products = self.json } }
  end
end)

-- Add product by json body
app:post("/products", json_params(function(self)
  local body = self.params
  local req_name  = body.name
  local req_category_id = body.category_id

  if not req_name or not req_category_id then
    return { json = { success = false, message = "Incorrect request parameters" }}
  end
  
  local product = Products:create({
    name = self.params.name,
    category_id = self.params.category_id
  })

  if product then
    return { json = { success = true, product = product }}
  else 
    return { json = { success = false, message = "Couldn't create product with given values" }}
  end
end))

return app
