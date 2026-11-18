const chatbot_container = document.getElementById('chatbot-container');
const user_container = document.getElementById('user-container');
const user_btn = document.getElementById('user-btn');

const ai_container = document.getElementById('ai-container');
const  ai_output = document.getElementById('ai-output');
const ai_name = document.getElementById('ai-name');

const user_input = document.getElementById('user-input');
const user_name = document.getElementById('user-name');
const error_msg = document.getElementById('error-msg');

 const new_ai_output = ai_output.cloneNode(true);

user_btn.addEventListener('click' ,async () => {
    if (user_input.value){
    error_msg.classList.remove('block');
    error_msg.classList.add('hidden');

     ai_container.classList.remove('hidden');
     ai_container.classList.add('flex');

     

    user_container.removeAttribute('id');
     user_name.removeAttribute('id');
    user_input.removeAttribute('id');
    user_btn.removeAttribute('id');
    error_msg.removeAttribute('id');

    user_btn.disabled = true;
    user_btn.classList.add('opacity-50')

    user_input.disabled = true;

    await connect_server(user_input.value, ai_output);
  
    
 
    chatbot();
    }else{
        error_msg.classList.remove('hidden');
        error_msg.classList.add('block');
    }
})

function chatbot(){

  

    

    //Remove the id from the old user container and assign it to the second one 
    
    const new_user_container = document.createElement('div');
    new_user_container.id = 'user-container';

    //Remove the ids of user input and user button elements

   
  
    //Copy user input and user button elements to new
    const new_user_name = user_name.cloneNode(true);
    const new_user_input = user_input.cloneNode(true);
    new_user_input.value = '';
    const new_user_btn = user_btn.cloneNode(true);
    const new_error_msg = error_msg.cloneNode(true);

    new_user_btn.disabled = false;
    new_user_btn.classList.remove('opacity-50');
    new_user_input.disabled = false;

    



    //Give the same ids to the new elements to repeat the chat again and again
    new_user_name.id = 'user-name';
    new_user_input.id = 'user-input';
    new_user_btn.id = 'user-btn';
    new_error_msg.id = 'error-msg';

    new_user_btn.addEventListener('click' ,async () => {
        if (new_user_input.value){
        new_error_msg.classList.remove('block');
            new_error_msg.classList.add('hidden');

        new_user_btn.disabled = true;
         new_user_btn.classList.add('opacity-50');


         new_user_input.disabled = true;

        ai_container.removeAttribute('id');
        const new_ai_container = document.createElement('div');
        new_ai_container.id = 'ai-container';
        new_ai_container.className = ai_container.className;

        const new_ai_name = ai_name.cloneNode(true);
       



        new_ai_name.id = 'ai-name';
        new_ai_output.id = 'ai-output';
        

        new_ai_container.appendChild(new_ai_name);
        new_ai_container.appendChild(new_ai_output);
        

        chatbot_container.appendChild(new_ai_container);
        
        new_ai_output.value = '';
        await connect_server(new_user_input.value, new_ai_output);

     
    

        chatbot()
        }
        else{
            new_error_msg.classList.remove('hidden');
            new_error_msg.classList.add('block');
        }

    })

    




    //Add the same styles and append them to the parent
    new_user_container.className = user_container.className;
    new_user_container.appendChild(new_user_name);
    new_user_container.appendChild(new_user_input);
    new_user_container.appendChild(new_error_msg);
    new_user_container.appendChild(new_user_btn);

  
   

    chatbot_container.appendChild(new_user_container);
}


async function connect_server(user_input, ai_output){
    const response = await fetch('/ai/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_input:user_input})
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();


         while (true) {
                const { value, done } = await reader.read();

                if (done) {
                    console.log('Stream completed.');
                    break;
                }

                const chunk = decoder.decode(value, { stream: true });
                 ai_output.value+=chunk
            }

        

       // const data = await response.json();
       // console.log(data.message);
       // if(!data.message){
       //     data.message = 'The server is not responed!';
      //  }
    //    return data.message;
    
}


window.addEventListener('DOMContentLoaded', () => {
   
    const navigationEntries = performance.getEntriesByType('navigation');

    if (navigationEntries.length > 0 && navigationEntries[0].type === 'reload') {
        user_input.value = "";
        ai_output.value = "";
        new_ai_output.value = "";
    }
});















/*
user_btn.addEventListener('click' , () => {
  
    chatbot(ai_container, user_container, user_btn);
})

async function chatbot(ai_container, user_container, user_btn) {
    if(user_input.value){
    error_msg.classList.remove('block');
    error_msg.classList.add('hidden');
    
    

    ai_container.classList.remove('hidden');
    ai_container.classList.add('flex');

        const response = await fetch('/ai/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_input:user_input.value})
        });

        const data = await response.json();
        console.log('Django Response:', data);
    
    
    
    user_container.removeAttribute('id');
    user_btn.removeAttribute('id');

    ai_container.removeAttribute('id');

    user_input.value = '';
    // 1. Clone ONLY the container (it already includes the child button inside it)
    const new_user_container = user_container.cloneNode(true);
    new_user_container.id = 'user-container';
    

    const new_ai_container = ai_container.cloneNode(true);
    new_ai_container.id = 'ai-container';

    // 2. Find the child button INSIDE the newly cloned container
    error_msg.removeAttribute('id');
    const new_user_btn = new_user_container.querySelector('button'); 
    
    new_user_container.appendChild(error_msg);
   
    if (new_user_btn) {
        new_user_btn.id = 'user-btn';
        new_user_btn.disabled = false;
        new_user_btn.classList.remove('opacity-50');

        // 3. Attach event listener directly to the nested button in the cloned DOM
        new_user_btn.addEventListener('click', () => {
            if(!user_input.value){
            chatbot_container.appendChild(new_ai_container);
            
            chatbot(ai_container, new_user_container, new_user_btn);
            }
            else{
                error_msg.classList.remove('hidden');
                error_msg.classList.add('block');

            }
        });
    }

    // 4. Append to DOM
    chatbot_container.appendChild(new_user_container);
    

    // Disable old button
    user_btn.disabled = true;
    user_btn.classList.add('opacity-50');

    }else{
        error_msg.classList.remove('hidden');
        error_msg.classList.add('block');
    }

}
*/



