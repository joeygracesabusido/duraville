// this function is to insert branch
const insert_branch = async () => {
    const data = {
        branch_code: document.getElementById("insert_branch_input").value
    
    };
    console.log(data)

    try {
        const response = await fetch(`/api-insert-branch-cost/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();
        console.log(responseData);
        
        if (response.ok){
            // Data saved successfully
            window.alert("Your data has been saved!!!!");
            // window.location.assign("/employee-transaction-grc/");
        }
        else {
            window.alert("Session has expired");
        }
        
    } catch (error) {
        window.alert("Duplicate Branch.");
        console.log(error);
    }
};

// Attach the event listener to the button
var Btn_branch_save = document.querySelector('#Bnt_save_branch');
Btn_branch_save.addEventListener("click", insert_branch);
