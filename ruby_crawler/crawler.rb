require "httparty"
require "nokogiri"
require "json"
require "watir"
require "mongo"

URL_BASE = "https://www.empik.com".freeze

client = Mongo::Client.new([ '127.0.0.1:27017' ], :database => 'crawler')
collection = client[:products]

puts "Please enter keyword to perform search: "
search_keyword = gets.chomp
puts "Searching www.empik.com with for products with keyword: #{search_keyword}"

response = HTTParty.get("https://www.empik.com/szukaj/produkt?q=#{search_keyword}&qtype=basicForm")
document = Nokogiri::HTML(response.body)

dynamic_browser = Watir::Browser.new :chrome

products = []
ShopProduct = Struct.new(:id, :nazwa, :kategorie, :cena, :obnizka, :szczegoly_towaru, :link)

document.css("div.search-list-item").each_with_index do |product, idx|
  product_link = URL_BASE + product.css("div.search-list-item-hover a").attribute("href")
  dynamic_browser.goto(product_link)
  inner_page = dynamic_browser.section(id: 'DetailedData').wait_until(&:present?)
  detailed_data = Nokogiri::HTML(inner_page.inner_html)

  detailed_info = {}

  detailed_data.css("table tbody tr").each do |detail|
    detailed_info[detail.css("th").text] = detail.css("td").text
  end

  new_product = ShopProduct.new(
    idx,
    product.attribute("data-product-name").text,
    product.attribute("data-product-category").text.split(" "),
    product.attribute("data-product-price").text,
    product.attribute("data-product-discount").text,
    detailed_info,
    product_link
  )
  collection.insert_one(new_product.to_h)
  products.push(new_product)

  if idx == 10 then
    break
  end
end

products.each do |product|
  puts product.to_h.to_json
end