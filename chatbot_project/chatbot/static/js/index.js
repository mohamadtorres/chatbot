async function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    let chatbox = document.getElementById("chatbox");

    if (userInput.trim() === "") return;

    let userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("user-message");
    userMessageDiv.innerText = userInput;
    chatbox.appendChild(userMessageDiv);
    document.getElementById("userInput").value = "";

    setTimeout(() => {
        chatbox.scrollTop = chatbox.scrollHeight;
    }, 10);

    // ✅ STEP 1: Show "Thinking..." immediately
    let botMessageContainer = document.createElement("div");
    botMessageContainer.classList.add("bot-message");

    let streamingMessage = document.createElement("span");
    streamingMessage.innerHTML = "🤖: <em>Thinking...</em>"; // ✅ Show immediately
    botMessageContainer.appendChild(streamingMessage);

    chatbox.appendChild(botMessageContainer);

    try {
        let response = await fetch("/chatbot/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        });

        let responseData = await response.json();
        let fullMessage = responseData.reply || "";
        let thoughtProcess = responseData.thought || "";

        // ✅ STEP 2: Insert Thought Process BEFORE bot message
        let thoughtContainer = document.createElement("div");
        thoughtContainer.classList.add("thought-container");
        thoughtContainer.innerHTML = `
            <button class="toggle-thought" onclick="toggleThought(this)" title="Show Thought Process">
                &#9660; Show Thought Process
            </button>
            <div class="thought-content" style="display: none;">
                <p><strong>Chatbot Thought Process:</strong></p>
                <p>${thoughtProcess}</p>
            </div>
        `;
        // ✅ Insert before the bot's message
        // ✅ Ensure the "Show Thought Process" appears **above** the bot message
        //✅ Ensure the "Show Thought Process" appears above the bot message
        chatbox.appendChild(botMessageContainer); // Add bot message first
        chatbox.insertBefore(thoughtContainer, botMessageContainer); /// Then append the bot message
        // ✅ Convert response to Markdown + Syntax Highlighting + KaTeX
        let formattedMessage = marked.parse(fullMessage);

        let tempDiv = document.createElement("div");
        tempDiv.innerHTML = formattedMessage;
        tempDiv.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });

        renderMathInElement(tempDiv, {
            delimiters: [
                { left: "$$", right: "$$", display: true },
                { left: "$", right: "$", display: false },
                { left: "\\(", right: "\\)", display: false },
                { left: "\\[", right: "\\]", display: true }
            ]
        });

        let finalMessage = tempDiv.innerHTML;

        // ✅ STEP 3: Simulate typing AFTER thought process
        await simulateStreaming(streamingMessage, finalMessage);

    } catch (error) {
        console.error("Error:", error);
        streamingMessage.innerHTML = `<p>Error: Unable to contact chatbot.</p>`;
    }
}






// ✅ Simulated streaming effect AFTER response is fully generated
async function simulateStreaming(element, formattedText) {
    let words = formattedText.split(" ");
    let displayedMessage = "🤖: ";

    for (let word of words) {
        displayedMessage += word + " ";
        element.innerHTML = displayedMessage;
        chatbox.scrollTop = chatbox.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 50)); // ✅ Typing delay
    }

    // ✅ Ensure MathJax renders properly
    setTimeout(() => {
        MathJax.typesetPromise();
    }, 300);
}

// ✅ Function to format responses with Markdown, Syntax Highlighting, and MathJax
function formatresponse(response) {
    if (!response) return "";

    const md = window.markdownit();
    let formattedResponse = md.render(response);

    // ✅ Convert `[ \boxed{...} ]` to `\[ \boxed{...} \]`
    formattedResponse = formattedResponse.replace(/\[\s*\\boxed{([^}]+)}\s*\]/g, "\\[ \\boxed{$1} \\]");

    // ✅ Convert `[ ... ]` inline math expressions into `\( ... \)`
    formattedResponse = formattedResponse.replace(/\[\s*([^]+?)\s*\]/g, "\\( $1 \\)");

    // ✅ Ensure `\text{}` is properly formatted inside inline math mode
    formattedResponse = formattedResponse.replace(/\\text{([^}]+)}/g, "\\(\\text{$1}\\)");

    // ✅ Force MathJax to process the response after insertion
    setTimeout(() => {
        MathJax.typesetPromise();
    }, 300);

    return formattedResponse;
}

// ✅ Toggle Thought Process Display
function toggleThought(button) {
    let content = button.nextElementSibling;
    
    if (content.style.display === "none") {
        content.style.display = "block"; // Show thought process
        button.innerHTML = "&#9650;"; // Change arrow to up (⬆)
        button.title = "Hide Thought Process";
    } else {
        content.style.display = "none"; // Hide thought process
        button.innerHTML = "&#9660;"; // Change arrow back to down (⬇)
        button.title = "Show Thought Process";
    }
}

// ✅ Detect Enter Key to Send Message
function handleKeyPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ✅ Copy Code from Code Blocks
function copyCode(button) {
    let codeBlock = button.parentElement.nextElementSibling.querySelector("code");
    let textArea = document.createElement("textarea");
    textArea.value = codeBlock.innerText;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);

    // ✅ Change button text temporarily to "Copied!"
    button.innerText = "Copied!";
    setTimeout(() => button.innerText = "Copy", 2000);
}

// ✅ Open Modal
function openModal(modalId) {
    let modal = document.getElementById(modalId);
    modal.style.display = "flex"; // ✅ Ensures proper alignment in the center
}

// ✅ Close Modal
function closeModal(modalId) {
    let modal = document.getElementById(modalId);
    modal.style.display = "none";
}

// ✅ Close Modal When Clicking Outside
window.onclick = function(event) {
    let modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
};
