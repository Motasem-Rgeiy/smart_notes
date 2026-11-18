document.getElementById('fetch-titles-btn').addEventListener('click', async (e) => {
    // === ADDED: Loading State Logic ===
    const fetchBtn = e.currentTarget;
    const originalBtnHTML = fetchBtn.innerHTML; // Save the original button design
    fetchBtn.disabled = true; // Disable button to prevent double clicks
    fetchBtn.classList.add('opacity-50', 'cursor-not-allowed'); // Make it look inactive
    fetchBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i><span>Loading...</span>'; // Change text to Loading
    
    try {
        const response = await fetch('/getNews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source: 'Hacker News' })
        });

        const data = await response.json();
        console.log('Django Response:', data);
        
        // === ADDED: Target the new modal list instead of the old container ===
        const main_title_ele = document.getElementById('titles-container'); // Kept untouched
        const modalContainer = document.getElementById('news-modal'); // Target the modal overlay
        const modalList = document.getElementById('modal-titles-container'); // Target the modal list
        
        modalList.innerHTML = ''; // Clear out any old titles from previous clicks

        data.data.forEach(element => {

            const row_ele = document.createElement('li')
            const title_ele = document.createElement('button');
            
            // === ADDED: Tailwind styling to make the dynamically created buttons look good in the modal ===
            title_ele.className = "w-full text-left bg-slate-800 hover:bg-slate-700 text-slate-200 p-3 rounded-lg text-sm transition";
            
            title_ele.textContent = element[0];
            title_ele.dataset.link = element[1];
            row_ele.append(title_ele);
            
            // === ADDED: Append to the modal list instead of the old main_title_ele ===
            modalList.append(row_ele) 
            
            console.log('outside:' ,element[0]);
            
            title_ele.addEventListener('click' , async (event) => {
                console.log('inside:' ,element[0]);
                
                // === ADDED: Hide the modal immediately when the user clicks a title ===
                modalContainer.classList.remove('flex');
                modalContainer.classList.add('hidden');
                
                const response = await fetch('/getData', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ source: 'Hacker News' , link:element[1] , title:element[0] })
                });

                const data = await response.json();
                console.log('Django Response:', data.status);
                if (data.status =='success'){
                    const message = document.getElementById('message');
                    message.classList.remove('hidden')
                    message.classList.add('flex');
                    setTimeout( ()=> {
                        message.classList.add('hidden');
                    }
                         , 3000
                        ) 
                }
            })
        });
        
        // === ADDED: Show the modal by replacing the 'hidden' class with 'flex' ===
        modalContainer.classList.remove('hidden');
        modalContainer.classList.add('flex');

    } catch (error) {
        console.error('Error fetching news:', error);
    } finally {
        // === ADDED: Revert button to normal after everything is done (even if it fails) ===
        fetchBtn.disabled = false;
        fetchBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        fetchBtn.innerHTML = originalBtnHTML; 
    }
});

// === ADDED: Close modal logic if the user decides to cancel by clicking 'Close' ===
document.getElementById('close-modal-btn').addEventListener('click', () => {
    const modalContainer = document.getElementById('news-modal');
    modalContainer.classList.remove('flex');
    modalContainer.classList.add('hidden');
});












/*
document.getElementById('fetch-titles-btn').addEventListener('click', async () => {
    try {
       
        const response = await fetch('/getNews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source: 'Hacker News' })
        });

        const data = await response.json();
        console.log('Django Response:', data);
        const main_title_ele = document.getElementById('titles-container');

        data.data.forEach(element => {

            const row_ele = document.createElement('li')
            const title_ele = document.createElement('button');
            title_ele.textContent = element[0];
            title_ele.dataset.link = element[1];
            row_ele.append(title_ele);
            main_title_ele.append(row_ele)
            console.log('outside:' ,element[0]);
            title_ele.addEventListener('click' , async (event) => {
                console.log('inside:' ,element[0]);
                const response = await fetch('/getData', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ source: 'Hacker News' , link:element[1] , title:element[0] })
            });

            const data = await response.json();
            console.log('Django Response:', data);
            })
            

           
        });
    } catch (error) {
        console.error('Error fetching news:', error);
    }
});

*/