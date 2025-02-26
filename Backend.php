<?php
// check_website.php

if (isset($_GET['url'])) {
    $url = $_GET['url'];
    $result = filter_website($url);
    echo $result;
} else {
    echo "No URL provided.";
}

function is_https($url) {
    return strpos($url, "https://") === 0;
}

function has_suspicious_keywords($url) {
    $keywords = ["malware", "phishing", "login", "free", "promo", "update", "gift", "offers"];
    foreach ($keywords as $word) {
        if (stripos($url, $word) !== false) {
            return true;
        }
    }
    return false;
}

function check_url_reputation($url) {
    $headers = @get_headers($url);
    return $headers && strpos($headers[0], '200') !== false;
}

function filter_website($url) {
    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        return "Invalid URL format!";
    }

    if (!is_https($url)) {
        return "Warning: The URL does not use HTTPS! This may not be secure.";
    }

    if (has_suspicious_keywords($url)) {
        return "Suspicious: The URL contains suspicious keywords.";
    }

    if (!check_url_reputation($url)) {
        return "Suspicious: The website might be down or unavailable.";
    }

    return "The website seems safe!";
}
?>
