<?php
/**
 * Secure Lock Solutions - Appointment Request Handler
 * Sends appointment requests to email
 */

// Set headers for JSON response
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit();
}

// Email configuration
$to_email = 'securelocksmithsolution@gmail.com';
$from_email = 'noreply@securelocksmithsolution.com';

// Get POST data
$category = isset($_POST['category']) ? htmlspecialchars($_POST['category']) : 'Not specified';
$service = isset($_POST['service']) ? htmlspecialchars($_POST['service']) : 'Not specified';
$phone = isset($_POST['phone']) ? htmlspecialchars($_POST['phone']) : 'Not provided';
$zip = isset($_POST['zip']) ? htmlspecialchars($_POST['zip']) : 'Not provided';
$address = isset($_POST['address']) ? htmlspecialchars($_POST['address']) : 'Not provided';
$additional_info = isset($_POST['additional_info']) ? htmlspecialchars($_POST['additional_info']) : 'None';
$timestamp = isset($_POST['timestamp']) ? htmlspecialchars($_POST['timestamp']) : date('g:i A n/j/Y');

// Validate required fields
if (empty($phone) || $phone === 'Not provided') {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Phone number is required']);
    exit();
}

// Build email subject
$subject = "🔐 New Appointment Request - {$service} | Secure Lock Solutions";

// Build HTML email body
$html_body = "
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }
        .header h1 { margin: 0; font-size: 24px; }
        .content { background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }
        .section { margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px; border-left: 4px solid #D4AF37; }
        .section h3 { margin: 0 0 10px 0; color: #D4AF37; }
        .info-row { margin: 8px 0; }
        .label { font-weight: bold; color: #555; }
        .value { color: #333; }
        .footer { background: #1a252f; color: #aaa; padding: 15px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }
        .urgent { background: #fff3cd; border-color: #ffc107; padding: 10px; border-radius: 5px; margin-top: 15px; }
        .phone-highlight { font-size: 20px; font-weight: bold; color: #D4AF37; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>🔐 New Appointment Request</h1>
            <p style='margin: 5px 0 0 0;'>Secure Lock Solutions</p>
        </div>
        
        <div class='content'>
            <div class='section'>
                <h3>📋 Service Details</h3>
                <div class='info-row'><span class='label'>Category:</span> <span class='value'>{$category}</span></div>
                <div class='info-row'><span class='label'>Service Requested:</span> <span class='value'>{$service}</span></div>
            </div>
            
            <div class='section'>
                <h3>👤 Customer Information</h3>
                <div class='info-row'><span class='label'>Phone:</span> <span class='value phone-highlight'>{$phone}</span></div>
                <div class='info-row'><span class='label'>Zipcode:</span> <span class='value'>{$zip}</span></div>
                <div class='info-row'><span class='label'>Address:</span> <span class='value'>{$address}</span></div>
            </div>
            
            <div class='section'>
                <h3>📝 Additional Notes</h3>
                <p>{$additional_info}</p>
            </div>
            
            <div class='section'>
                <h3>🕐 Submission Details</h3>
                <div class='info-row'><span class='label'>Submitted:</span> <span class='value'>{$timestamp}</span></div>
                <div class='info-row'><span class='label'>Source:</span> <span class='value'>Website Appointment Form</span></div>
            </div>
            
            <div class='urgent'>
                <strong>⚡ Action Required:</strong> Please contact the customer as soon as possible.
            </div>
        </div>
        
        <div class='footer'>
            <p>Secure Lock Solutions | Orange County, CA</p>
            <p>This is an automated message from your website appointment form.</p>
        </div>
    </div>
</body>
</html>
";

// Build plain text email body (fallback)
$plain_body = "
NEW APPOINTMENT REQUEST - SECURE LOCK SOLUTIONS
================================================

SERVICE DETAILS:
- Category: {$category}
- Service: {$service}

CUSTOMER INFORMATION:
- Phone: {$phone}
- Zipcode: {$zip}
- Address: {$address}

ADDITIONAL NOTES:
{$additional_info}

SUBMISSION DETAILS:
- Submitted: {$timestamp}
- Source: Website Appointment Form

================================================
Please contact the customer as soon as possible.
";

// Email headers
$headers = array(
    'MIME-Version: 1.0',
    'Content-type: text/html; charset=UTF-8',
    'From: Secure Lock Solutions <' . $from_email . '>',
    'Reply-To: ' . $from_email,
    'X-Mailer: PHP/' . phpversion(),
    'X-Priority: 1',
    'Importance: High'
);

// Send email
$email_sent = mail($to_email, $subject, $html_body, implode("\r\n", $headers));

// Also send to a backup email if needed (optional)
// $backup_email = 'backup@example.com';
// mail($backup_email, $subject, $html_body, implode("\r\n", $headers));

// Log the submission (optional - create a log file)
$log_file = 'appointment_log.txt';
$log_entry = date('Y-m-d H:i:s') . " | Phone: {$phone} | Service: {$service} | Email Sent: " . ($email_sent ? 'Yes' : 'No') . "\n";
file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);

// Return response
if ($email_sent) {
    echo json_encode([
        'success' => true,
        'message' => 'Appointment request submitted successfully!'
    ]);
} else {
    // Email failed but we still want the form to appear successful to the user
    // The Telegram backup should still work
    echo json_encode([
        'success' => true,
        'message' => 'Request received. We will contact you shortly.',
        'email_status' => 'pending'
    ]);
}
?>
