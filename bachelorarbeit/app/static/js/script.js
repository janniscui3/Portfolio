// Function to make a fetch request and handle response errors
async function makeFetchRequest(url, options) {
    const response = await fetch(url, options);
    
    if (!response.ok) {
        throw new Error("HTTP error! Status: " + response.status);
    }

    return response.json();
}

// Function to fetch sentences based on selected category and sentiment
async function fetchSentenceDatabase() {

    // Get the selected value from the dropdown
    const selectedCategory = document.getElementById("databaseDropdown").value;
    const selectedSentiment = document.getElementById("sentimentDatabaseDropdown").value;
    try {
        const url = "/api/fetch_sentence?category=" + selectedCategory + "&sentiment=" + selectedSentiment;
        const data = await makeFetchRequest(url);
        
        console.log("Fetched sentence:", data.result);
        document.getElementById("resultContentDatabase").value = data.result;
    } catch (error) {
        console.error("Error fetching sentence:", error);
    }
}

// Function to process text using a specified API endpoint
async function processText(apiEndpoint, textareaId, resultId) {
    // Get the text from the textarea
    const text = document.getElementById(textareaId).value;

    try {
        const url = "/api/" + apiEndpoint;
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: text }),
        };

        const data = await makeFetchRequest(url, options);

        console.log("Processed result:", data.result);
        document.getElementById(resultId).value = data.result;
    } catch (error) {
        console.error("Error processing text:", error);
    }
}

// Function to process text on locally hosted model
function processTextLocalHost() {
    processText("process_text", "textareaLocalHost", "resultLocalHost");
}

// Function to process text on a cloud host
function processTextCloudHost() {
    processText("process_text_external", "textareaCloudHost", "resultCloudHost");
}