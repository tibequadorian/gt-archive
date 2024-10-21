<?php
$errorMessage = ''; // Variable for error messages
if (isset($_GET['query'])) {
    $query = $_GET['query'];
    $pattern = '/^https?:\/\/www\.goettinger-tageblatt\.de\/.*-([A-Z0-9]{26})\.html$/';
    if (preg_match($pattern, $query, $matches)) {
        $filenamePart = $matches[1];
        $filename = "./archive/" . $filenamePart . ".html";
        if (file_exists($filename)) {
            header("Location: $filename");
            exit();
        } else {
            $errorMessage = "Not found.";
        }
    } else {
        $errorMessage = "Invalid URL.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GT-Archive</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 100vh;
            margin: 0;
        }
        input[type="text"] {
            width: 400px;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <form method="GET">
        <input type="text" name="query" placeholder="URL" required>
        <input type="submit" value="Search">
    </form>

    <p class="error"><?= htmlspecialchars($errorMessage) ?></p>
</body>
</html>
