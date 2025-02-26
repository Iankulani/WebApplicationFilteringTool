# app.rb
require 'sinatra'
require 'net/http'
require 'uri'

get '/check_website' do
  url = params[:url]
  result = filter_website(url)
  result
end

def is_https(url)
  url.start_with?("https://")
end

def has_suspicious_keywords(url)
  suspicious_keywords = ["malware", "phishing", "login", "free", "promo", "update", "gift", "offers"]
  suspicious_keywords.any? { |word| url.downcase.include?(word) }
end

def check_url_reputation(url)
  uri = URI.parse(url)
  response = Net::HTTP.get_response(uri)
  response.is_a?(Net::HTTPSuccess)
rescue
  false
end

def filter_website(url)
  return "Invalid URL format!" unless URI.regexp.match?(url)

  unless is_https(url)
    return "Warning: The URL does not use HTTPS! This may not be secure."
  end

  if has_suspicious_keywords(url)
    return "Suspicious: The URL contains suspicious keywords."
  end

  unless check_url_reputation(url)
    return "Suspicious: The website might be down or unavailable."
  end

  "The website seems safe!"
end
