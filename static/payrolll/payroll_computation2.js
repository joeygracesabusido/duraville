// $(document).ready(function() {
//     $("#name").autocomplete({
//         source: function(request, response) {
//             $.ajax({
//                 url: "/employee-with-deductions/",
//                 data: { term: request.term },
//                 dataType: "json",
//                 success: function(data) {
//                     response(data);
//                 },
//                 error: function(err) {
//                     console.error("Error fetching autocomplete data:", err);
//                     // Optionally, provide user feedback about the error
//                 }
//             });
//         },
//         minLength: 0,  // Minimum length of the input before triggering autocomplete
//         select: function(event, ui) {
//             $("#name").val(ui.item.value); 
//             $("#employee_id_id").val(ui.item.id);
//             $("#basic_pay").val(ui.item.basic_monthly_pay / 2);
//             $("#sss_loan").val(Number(ui.item.total_sss_loan_deduction).toFixed(2));
//             $("#hdmf_loan").val(Number(ui.item.total_hdmf_loan_deduction).toFixed(2));
//             $("#general_loan").val(Number(ui.item.total_cash_advance).toFixed(2));
//             return false;
//         }
//     });

  
// });

// this is for autocomplete using graphql

$( function() {
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
    
    $("#name").autocomplete({
      source: function( request, response ) {
        $.ajax({
          url: "/graphql",
          dataType: "json",
          data: {
            query: `
              query {
                getEmployeeWithDeductions2(term: "${extractLast(request.term)}") {
                  name
                  totalCashAdvance
                  totalHdmfLoanDeduction
                  totalSssLoanDeduction
                  id
                  basicMonthlyPay
                  books
                }
              }
            `
          },
          success: function( data ) {
            response( data.data.getEmployeeWithDeductions2.map(function(item) {
              return {
                label: item.name,
                value: item.name,
                id: item.id,
                basicMonthlyPay: item.basicMonthlyPay,
                totalCashAdvance: item.totalCashAdvance,
                totalSssLoanDeduction: item.totalSssLoanDeduction,
                totalHdmfLoanDeduction: item.totalHdmfLoanDeduction,
                books: item.books
              };
            }));
          }
        });
      },
      minLength: 2,
      select: function( event, ui ) {
        $("#name").val(ui.item.value);
        $("#employee_id_id").val(ui.item.id);
        $("#basic_pay").val(ui.item.basicMonthlyPay / 2);
        $("#sss_loan").val(Number(ui.item.totalSssLoanDeduction).toFixed(2));
        $("#hdmf_loan").val(Number(ui.item.totalHdmfLoanDeduction).toFixed(2));
        $("#general_loan").val(Number(ui.item.totalCashAdvance).toFixed(2));
        $("#books").val(ui.item.books);
        calculatetotalGross();
        calculatetotalDeduction()
        calculatetotalNetpay()
        return false;
      }
    });
  });














// this is for computation of gross payroll

$(document).ready(function() {
    $('#basic_pay,#late,#absent,#under_time,#normal_working_day_ot, \
        #holiday_ot,#basic_pay_adjustment,#spl_30,#legal_holiday').on('input', function() {
        calculatetotalGross();
        calculatetotalDeduction()
    });
    });

    function calculatetotalGross() {
    
    let basic_pay;
    let late;
    let absent;
    let under_time;
    let normal_working_day_ot;
    let holiday_ot;
    let basic_pay_adjustment;
    let spl_30;
    let legal_holiday;
   


    basic_pay = $('#basic_pay').val() || 0;
    late = $('#late').val() || 0;
    absent = $('#absent').val() || 0;
    under_time = $('#under_time').val() || 0;
    normal_working_day_ot = $('#normal_working_day_ot').val() || 0;
    holiday_ot = $('#holiday_ot').val() || 0;
    basic_pay_adjustment = $('#basic_pay_adjustment').val() || 0;
    spl_30 = $('#spl_30').val() || 0;
    legal_holiday = $('#legal_holiday').val() || 0;
    
    
    let product;
    let product2
    product = (parseFloat(basic_pay) + parseFloat(late)
                    + parseFloat(absent) + parseFloat(under_time)
                    + parseFloat(normal_working_day_ot) + parseFloat(holiday_ot)
                    + parseFloat(basic_pay_adjustment)
                    + parseFloat(spl_30)
                    + parseFloat(legal_holiday));

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#gross_pay').val(stringNumber);
    $('#gross_pay2').val(product2);
    
   
    calculatetotalNetpay()

    }


// this is for computation of total deduction

$(document).ready(function() {
    $('#housing_loan,#sss_loan,#hdmf_loan,#general_loan,#company_loan,#other_adjustment').on('input', function() {
        calculatetotalDeduction();
        calculatetotalNetpay();
    });
    });

    function calculatetotalDeduction() {
    
    let housing_loan;
    let sss_loan;
    let hdmf_loan;
    let general_loan;
    let company_loan;
    let other_adjustment;
   
   


    housing_loan = $('#housing_loan').val() || 0;
    sss_loan = $('#sss_loan').val() || 0;
    hdmf_loan = $('#hdmf_loan').val() || 0;
    general_loan = $('#general_loan').val() || 0;
    company_loan = $('#company_loan').val() || 0;
    other_adjustment =  $('#other_adjustment').val() || 0;
    
    
    
    let product;
    let product2
    product = (parseFloat(housing_loan) + parseFloat(sss_loan)
                    + parseFloat(hdmf_loan) + parseFloat(general_loan)
                    + parseFloat(company_loan) + parseFloat(other_adjustment)
                    );

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#total_deduction').val(stringNumber);
    $('#total_deduction2').val(product2);
   
    }


// this is for computation of NET PAY

    $(document).ready(function() {
        $('#gross_pay2,#total_deduction2,#adjustment_non_tax').on('input', function() {
            calculatetotalDeduction();
            calculatetotalNetpay();
            
        });
        });

        function calculatetotalNetpay() {
        
        let gross_pay2;
        let total_deduction2;
        let adjustment_non_tax;
        
    
  
        gross_pay2 = $('#gross_pay2').val() || 0;
        total_deduction2 = $('#total_deduction2').val() || 0;
        adjustment_non_tax = $('#adjustment_non_tax').val() || 0;
        
        
        
        let product;
        let product2;
        product = (parseFloat(gross_pay2) - parseFloat(total_deduction2) + parseFloat(adjustment_non_tax)
                        );

        product2 = product.toFixed(2);
        const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        $('#net_pay').val(stringNumber);
        $('#net_pay2').val(product2);
        }


// this function is for saving payroll

const savePayrollComputation = () => {
  const data = {
      date_from: document.getElementById("date_from").value,
      date_to: document.getElementById("date_to").value,
      payroll_date: document.getElementById("payroll_date").value,
      books: document.getElementById("books").value,
      employee_specs: document.getElementById("employee_specs").value,
      basic_pay: document.getElementById("basic_pay").value,
      late: document.getElementById("late").value || 0,
      absent: document.getElementById("absent").value || 0,
      undertime: document.getElementById("under_time").value || 0,
      normal_working_day_ot: document.getElementById("normal_working_day_ot").value || 0,
      spl_30: document.getElementById("spl_30").value || 0,
      legal: document.getElementById("legal_holiday").value || 0,
      holiday_ot: document.getElementById("holiday_ot").value || 0,
      basic_pay_adjustment: document.getElementById("basic_pay_adjustment").value || 0,
      gross_pay: document.getElementById("gross_pay2").value,
      housing_loan: document.getElementById("housing_loan").value || 0,
      sss_loan: document.getElementById("sss_loan").value || 0,
      hdmf_loan: document.getElementById("hdmf_loan").value || 0,
      general_loan: document.getElementById("general_loan").value || 0,
      company_loan: document.getElementById("company_loan").value || 0,
      other_adjustment: document.getElementById("other_adjustment").value || 0,
      total_deduction: document.getElementById("total_deduction2").value || 0,
      net_pay: document.getElementById("net_pay2").value || 0,
      employee_id_id: document.getElementById("employee_id_id").value ,
      adjustment_not_taxable: document.getElementById("adjustment_non_tax").value || 0
     
      
  };

  fetch('/api-insert-payroll-activity/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      else{
        alert('Data has been Save')
      }
      return response.json();
  })
  .then(data => {
      console.log(data);
      // Do something with the response data
  })
  .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
  });
};

document.getElementById("btn_save_payroll_computation").addEventListener("click", savePayrollComputation);