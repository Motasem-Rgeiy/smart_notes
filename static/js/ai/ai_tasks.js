const user_content = document.getElementById('content');

const summarize_btn = document.getElementById('summarize-btn');
const rewrite_btn = document.getElementById('rewrite-btn');
const extract_btn = document.getElementById('extract-btn');
const suggest_btn = document.getElementById('suggest-btn');

const output_content = document.getElementById('output-content');
const ai_box = document.getElementById('ai_box');

//1-listen for all of buttons
//2- each of the listener has the same function with different params values 


summarize_btn.addEventListener('click', async (e) => {
   
    const system_settings = 'Summarize the input content to be in shorter, it is saved as a note for the user.';
    const user_content_input = user_content.dataset.content;
     ai_call(e , system_settings , user_content_input);
})


rewrite_btn.addEventListener('click', async (e) => {
   
    const system_settings = 'You are provided by the a note content, You have to rewrite the content in sorted way.';
    const user_content_input = user_content.dataset.content;
     ai_call(e , system_settings , user_content_input);
})



extract_btn.addEventListener('click', async (e) => {
   
    const system_settings = 'You are provided by the a note content, Extract the most important points from the content and return it back in points.';
    const user_content_input = user_content.dataset.content;
     ai_call(e , system_settings , user_content_input);
})




suggest_btn.addEventListener('click', async (e) => {
   
    const system_settings = 'You are provided by the a note content, give me a suggested titles. You have to write only the titles, each one in a signle line without any extra lines or titles from you.';
    const user_content_input = user_content.dataset.content;
     ai_call(e , system_settings , user_content_input);
})







async function ai_call(e , system_settings , user_content_input){


    const aiBtn = e.currentTarget;
    const originalBtnHTML = aiBtn.innerHTML;
    



    // 1. Disable button UI
    aiBtn.disabled = true;
    aiBtn.classList.add('opacity-50', 'cursor-not-allowed');
    aiBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i><span>Loading...</span>';

    try {
        if (user_content.dataset.content) {
            

            const response = await fetch('/ai/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    content: user_content_input, 
                    system_settings: system_settings 
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            // Clear old output and show output box before streaming starts
            output_content.textContent = '';
            ai_box.classList.remove('hidden');
            ai_box.classList.add('flex');

            // 2. Stream loop
            while (true) {
                const { value, done } = await reader.read();

                if (done) {
                    console.log('Stream completed.');
                    break;
                }

                // Decode and append chunk INSIDE the loop
                const chunk = decoder.decode(value, { stream: true });
                output_content.textContent += chunk;
            }
        }
    } catch (error) {
        console.error('Streaming failed:', error);
    } finally {
        // 3. Reset button UI (runs on both success and error)
        aiBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        aiBtn.disabled = false;
        aiBtn.innerHTML = originalBtnHTML;
    
}
}