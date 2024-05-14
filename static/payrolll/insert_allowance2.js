$(document).ready(function() {
    $("#name").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-acutocomplte-employee/",
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
            $("#name").val(ui.item.value);
            
            $("#employee_id_id").val(ui.item.id);

            return false;
        }
    });

  
});


// this function is to insert allowance
// Arrow function to handle form submission
const insert_allowance = () => {
    // Get form values
    const payroll_date = $("#payroll_date").val();
    const user = $("#user").val();
    const allowance = $("#allowance").val() || 0;
    const meal_allowance = $("#meal_allowance").val() || 0;
    const developmental = $("#developmental").val() || 0;
    const holiday_rdot_pay = $("#holiday_rdot_pay").val() || 0;
    const allowance_deduction = $("#allowance_deduction").val() || 0;
    const allowance_adjustment = $("#allowance_adjustment").val() || 0;
    const employee_id_id = $("#employee_id_id").val();

    // Send data to GraphQL endpoint using AJAX
    $.ajax({
      url: '/graphql',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        query: `
          mutation {
            insertAllowance(
              employeeIdId: ${employee_id_id},
              allowance: ${allowance},
              mealAllowance: ${meal_allowance},
              developmental: ${developmental},
              holidayRdotPay: ${holiday_rdot_pay},
              allowanceDeduction: ${allowance_deduction},
              allowanceAdjustment: ${allowance_adjustment},
              payrollDate: "${payroll_date}",
              user: "${user}"
            )
          }
        `
      }),
      success: (response) => {
        // Handle success response
        console.log(response);
        // Optionally, display a success message to the user
        window.alert("Data Has Been Save");
        window.location.href = '/frame-allowance/';
      },
      error: (error) => {
        // Handle error response
        console.error(error);
        // Optionally, display an error message to the user
      }
    });
  };

  // Event listener for form submission
  $(document).ready(() => {
    $("#btn_save_allowance").click((event) => {
      event.preventDefault(); // Prevent default form submission
      insert_allowance(); // Call the submitForm function
    });
  });


// this function is to display data of allowance


$(document).ready(function() {
    $.ajax({
        type: 'POST',
        url: '/graphql', // Change this to your GraphQL endpoint
        contentType: 'application/json',
        data: JSON.stringify({
            query: `query MyQuery {
                getAllowanceList {
                  payrollDate
                  name
                  allowance
                  mealAllowance
                  developmental
                  holidayRdotPay
                  allowanceAdjustment
                  allowanceDeduction
                }
              }`
        }),
        success: function(response) {
            var data = response.data.getAllowanceList;
            var tableBody = $('#my_table_allowance');
            tableBody.empty();

            data.forEach(function(item) {
                var formattedAllowance = parseFloat(item.allowance).toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });

                var formatedmealAllowance = parseFloat(item.mealAllowance).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
              });
                var row = '<tr>' +
                    '<td>' + item.payrollDate + '</td>' +
                    '<td>' + item.name + '</td>' +
                    '<td>' + formattedAllowance + '</td>' +
                    '<td>' + formatedmealAllowance + '</td>' +
                    '<td>' + item.developmental + '</td>' +
                    '<td>' + item.holidayRdotPay + '</td>' +
                    '<td>' + item.allowanceDeduction + '</td>' +
                    '<td>' + item.allowanceAdjustment + '</td>' +
                    '</tr>';
                tableBody.append(row);
            });

            initializeDataTable();
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
});

const initializeDataTable = () => {
    $('#my_table_allowance2').DataTable();
};



function formatNumber(number) {
  // Check if the number is valid
  if (isNaN(number)) {
      return number; // Return as is if not a valid numbergit add 
  }
  
  // Format number with thousand separator and 2 decimal places
  return parseFloat(number).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}


function payrollListExcel(type){
    var data = document.getElementById('my_table_allowance2');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'allowanceList.' + type);

  }

