$(document).ready(function() {
    $("#book").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-search-autocomplete-books/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                },
                error: function(err) {
                    console.error("Error fetching autocomplete data:", err);
                    // Optionally, provide user feedback about the error
                }
            });
        },
        minLength: 0,  // Minimum length of the input before triggering autocomplete
        select: function(event, ui) {
            $("#book").val(ui.item.value);
            $("#company_id").val(ui.item.company_id);
            $("#book_id").val(ui.item.id);

            return false;
        }
    });

  
});





// this function is to update for employee details

const update_employee_details = async () => {
    const id = document.getElementById("trans_id").value; // Assigning id correctly
    basic_monthly_pay = parseFloat(document.getElementById("basic_monthly_pay").value || 0);
    const data = {
        
        employee_id: document.getElementById("employee_id").value,
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        basic_monthly_pay: basic_monthly_pay,
        tax_code: document.getElementById("tax_code").value,
        book_id: document.getElementById("book_id").value,
        department: document.getElementById("department").value,
        is_active: document.getElementById("is_active").value,
        company_id: document.getElementById("company_id").value
    };

    console.log(data.basic_monthly_pay)
    
    try {
        const response = await fetch(`/api-update-employee-details/` + id, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            console.log(responseData);
            // Data saved successfully
            window.alert("Your data has been saved!!!!");
            // Optionally, you can redirect to another page
            window.location.assign("/insert-employee-list/");
        } else if (response.status === 401) {
            // Unauthorized, session has expired
            window.alert("Session has expired");
        } else if (response.status === 400) {
            // Bad Request, duplicate branch
            const responseData = await response.json();
            window.alert(`Error: ${responseData.detail}`);
        } else {
            // Handle other errors
            window.alert("An unexpected error occurred");
        }
    } catch (error) {
        // Handle unexpected errors
        window.alert("An unexpected error occurred");
        console.log(error);
    }
};

// Attach the event listener to the button
const Btn_save_employee_list = document.querySelector('#btn_save_employee');
Btn_save_employee_list.addEventListener("click", update_employee_details);


// const update_employee_details = async () => {
//     const id = $("#trans_id").val(); // Assigning id correctly
    
//     const data = {
//         employee_id: $("#employee_id").val(),
//         first_name: $("#first_name").val(),
//         last_name: $("#last_name").val(),
//         basic_monthly_pay: $("#basic_monthly_pay").val(),
//         tax_code: $("#tax_code").val(),
//         book_id: $("#book_id").val(),
//         department: $("#department").val(),
//         is_active: $("#is_active").val(),
//         company_id: $("#company_id").val()
//     };
//     console.log(data)
//     try {
//         const response = await fetch(`/api-update-employee-details/${id}`, {
//             method: "PUT",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify(data),
//         });

//         if (response.ok) {
//             const responseData = await response.json();
//             console.log(responseData);
//             // Data saved successfully
//             window.alert("Your data has been saved!!!!");
//             // Optionally, you can redirect to another page
//             // window.location.assign("/insert-employee-list/");
//         } else if (response.status === 401) {
//             // Unauthorized, session has expired
//             window.alert("Session has expired");
//         } else if (response.status === 400) {
//             // Bad Request, duplicate branch
//             const responseData = await response.json();
//             window.alert(`Error: ${responseData.detail}`);
//         } else {
//             // Handle other errors
//             window.alert("An unexpected error occurred");
//         }
//     } catch (error) {
//         // Handle unexpected errors
//         window.alert("An unexpected error occurred");
//         console.log(error);
//     }
// };

// // Attach the event listener to the button
// $("#btn_save_employee").on("click", update_employee_details);

