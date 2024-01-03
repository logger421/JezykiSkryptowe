local lapis = require("lapis")
local Model = require("lapis.db.model").Model
local json_params = require("lapis.application").json_params
local respond_to = require("lapis.application").respond_to

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

app:match("/categories", respond_to({
  -- Get all categories
    GET = function(self)
      self.json = Categories:select()
      return { json = { success = true, category = self.json } }
    end,
  -- Add category by json body
    POST = json_params(function(self)
      local req_name = self.params.name

      if not req_name then
        return { json = { success = false, message = "Incorrect request parameter"}}
      end
      local category = Categories:create({
        name = req_name
      })

      if not category then
        return { json = { success = false, message = "Couldn't create category with given values" }}
      else
        return { json = { success = true, category = category}}
      end
    end)
  }))

app:get("/categories/:id[%d]", function (self)
  self.json = Categories:find(self.params.id)
  if self.json then
    return { json = { success = true, category = self.json }}
  else
    return { json = { success = false, message = "Category for given id doesn't exists!" }}
  end
end)

-- Get products by category they belong (named)
app:get("/categories/:category", function(self)
  local categoryDAO = Categories:find({ name = self.params.category })
  if not categoryDAO then
    return { json = { success = false, message = "No such category, products can't be listed!" }}
  else 
    self.json = Products:select("where category_id = ?", categoryDAO["id"])
    return { json = { success = true, products = self.json } }
  end
end)

app:match("/products", respond_to({
-- Get all products
  GET = function(self)
    self.json = Products:select()
    return { json = { success = true, product = self.json } }
  end,
-- Add product by json body
  POST = json_params(function(self)
    local body = self.params
    local req_name  = body.name
    local req_category_id = body.category_id

    if not req_name or not req_category_id then
      return { json = { success = false, message = "Incorrect request parameters" }}
    end
  
    local product = Products:create({
      name = req_name,
      category_id = req_category_id
    })

    if product then
      return { json = { success = true, product = product }}
    else 
      return { json = { success = false, message = "Couldn't create product with given values" }}
    end
  end)
}))

-- Get product by id
app:get("/products/:id[%d]", function (self)
  self.json = Products:find(self.params.id)
  if not self.json then
    return { json = { success = false, message = "Category for given id doesn't exists!" }}
  else
    return { json = { success = true, product = self.json } }
  end
end)

return app
