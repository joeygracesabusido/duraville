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
       
        $("#books").val(ui.item.books);

        // const basicPayValue = $("#basic_pay").val();
       
        

        calculatetotalGross();
        BtnMandatory();
        calculatetotalDeduction();
        calculatetotalNetpay();
        last_cutoff_gross();
        // with_tax_calculation();
       
        return false;
      }
    });
  });



  // this is for autocomplete of sss

    function BtnMandatory() {
      const searchBasicPay = ($("#basic_pay").val()) * 2; // Get the value of the input field
      const getSSSQuery = `
        query {
          getSssTable(amount: ${searchBasicPay}) {
            employeeShares
            employerShare
            ssProvidentEmp
            ssProvidentEmpr
            ecc
          }
        }
      `;
  
      $.ajax({
        url: "/graphql",
        method: "POST",
        data: JSON.stringify({ query: getSSSQuery }),
        contentType: "application/json",
        success: function(data) {
          const empshares = data.data.getSssTable.map(item => item.employeeShares);
          const ssProvidentEmp = data.data.getSssTable.map(item => item.ssProvidentEmp);
         
         
          $("#sss").val(empshares);
          $("#sss_provident").val(ssProvidentEmp);
          
         
          

          let basicPayValue = $("#basic_pay").val();
          let phic_com;
          let hdmf_comp;

          hdmf_comp = 200
          if ((basicPayValue * 2) <= 10000){
            phic_com =  500 / 2
            // phic_come = phic_com.toFixed(2)
            $("#phic").val(phic_com);
          } else if ((basicPayValue * 2) > 10000 && (basicPayValue * 2)<=100000) {
            phic_com =  (basicPayValue * 2) * 0.05 / 2
            // phic_come = phic_com.toFixed(2)
            $("#phic").val(phic_com);
          } else {
            phic_com = 5000 / 2
          }
          
          $("#hdmf").val(hdmf_comp);

         
         
          // last_cutoff_gross()
          calculatetotalDeduction()
          
          calculatetotalNetpay();
          
        },
        error: function(xhr, status, error) {
          console.error("Request failed:", error);
        }
      });
    }


   // this is for autocomplete of sss

      // function last_cutoff_gross() {
      //   const search_employee_id = ($("#employee_id_id").val()) ; // Get the value of the input field
      //   const search_payroll_date = ($("#payroll_date_last_cut_off").val()) ; // Get the value of the input field
      //   const getGrossLastPayroll = `
      //     query {
      //       getApiPayrollForTaxComp(employeeIdSearch: ${search_employee_id},payrollDate: "${search_payroll_date}") {
      //         grossPay
      //       }
      //     }
      //   `;

      //   $.ajax({
      //     url: "/graphql",
      //     method: "POST",
      //     data: JSON.stringify({ query: getGrossLastPayroll }),
      //     contentType: "application/json",
      //     success: function(data) {
      //       const last_gross_payroll = data.data.getApiPayrollForTaxComp.map(item => item.grossPay);
      //       $("#grosspay_last_cut_off").val(last_gross_payroll);

      //       with_tax_calculation()

                   
      //     },
      //     error: function(xhr, status, error) {
      //       console.error("Request failed:", error);
      //     }
      //   });
      // }


      const last_cutoff_gross = () => {
        const search_employee_id = $("#employee_id_id").val(); // Get the value of the input field
        const search_payroll_date = $("#payroll_date_last_cut_off").val(); // Get the value of the input field
        const getGrossLastPayroll = `
            query {
                getApiPayrollForTaxComp(employeeIdSearch: ${search_employee_id}, payrollDate: "${search_payroll_date}") {
                    grossPay
                }
            }
        `;
    
        $.ajax({
            url: "/graphql",
            method: "POST",
            data: JSON.stringify({ query: getGrossLastPayroll }),
            contentType: "application/json",
            success: (data) => {
                const last_gross_payroll = data.data.getApiPayrollForTaxComp.map(item => item.grossPay);
                $("#grosspay_last_cut_off").val(last_gross_payroll);
    
                with_tax_calculation();
            },
            error: (xhr, status, error) => {
                console.error("Request failed:", error);
            }
        });
    };
    





  // // Or call the function when a button is clicked
  // $("#search_button").on("click", function() {
  //   BtnMandatory();
  // });
  

// this is for computation of with holding tax
$(document).ready(function() {
  $('#grosspay_last_cut_off,#sss,#sss_provident,#phic,#hdmf').on('input', function() {
      with_tax_calculation();
  });
});

function with_tax_calculation() {
  let sss = parseFloat($('#sss').val()) || 0;
  let sss_provident = parseFloat($('#sss_provident').val()) || 0;
  let phic = parseFloat($('#phic').val()) || 0;
  let hdmf = parseFloat($('#hdmf').val()) || 0;
  let total_gross1 = parseFloat($('#grosspay_last_cut_off').val()) || 0;
  let total_gross2 = parseFloat($('#gross_pay2').val()) || 0;
  let total_mandatory = sss + sss_provident + phic + hdmf;
  let grand_total_gross = parseFloat(total_gross1) + parseFloat(total_gross2);
  let tax_base_amount = parseFloat(grand_total_gross) - parseFloat(total_mandatory);

  // console.log(total_mandatory)
  // console.log(total_gross2)
  // console.log(tax_base_amount)
  // Define your tax brackets and rates
  const bracket_1 = [0, 20833];
  const bracket_2 = [20833.01, 33333];
  const bracket_3 = [33333.01, 66666];
  const bracket_4 = [66667, 166666];
  const bracket_5 = [166667, 666666];
  // ... Add more rates corresponding to the brackets

  // Apply tax rates based on the income brackets
  const tax = [];

  for (let income of [tax_base_amount]) {
      let incomeTax = 0;
      if (income > bracket_1[0] && income <= bracket_1[1]) {
          incomeTax = parseFloat((income * 0).toFixed(2));
      } else if (income > bracket_2[0] && income <= bracket_2[1]) {
          incomeTax = parseFloat(((income - 20833) * 0.15).toFixed(2));
      } else if (income > bracket_3[0] && income <= bracket_3[1]) {
          incomeTax = parseFloat(((income - 33333) * 0.20 + 1875).toFixed(2));
      } else if (income > bracket_4[0] && income <= bracket_4[1]) {
        incomeTax = parseFloat(((income - 66666) * 0.25 + 8541.80).toFixed(2));
    } else if (income > bracket_5[0] && income <= bracket_5[1]) {
      incomeTax = parseFloat(((income - 166667) * 0.30 + 33541.80).toFixed(2));
  } 

      tax.push(incomeTax);
  }

  let stringNumber = tax[0].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  
  $('#tax_withheld').val(tax);
}


  
  


// this is for computation of gross payroll
  $(document).ready(function() {
    $('#basic_pay,#late,#absent,#under_time,#normal_working_day_ot, \
        #holiday_ot,#basic_pay_adjustment,#spl_30,#legal_holiday').on('input', function() {
        calculatetotalGross();
        calculatetotalDeduction()
        calculatetotalNetpay();
        with_tax_calculation();
       
        
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
    
    }


    // this is for computation of total deduction

$(document).ready(function() {
    $('#sss,#sss_provident,#phic,#hdmf,#other_adjustment,#tax_withheld,#general_loan,#company_loan').on('input', function() {
        // with_tax_calculation();
        BtnMandatory();
       
        calculatetotalDeduction();
        // calculatetotalNetpay();
       
       
    });
    });

    function calculatetotalDeduction() {
     
    
    let sss;
    let sss_provident;
    let phic;
    let hdmf;
    let tax_withheld;
    let other_adjustment;
    let general_loan;
    let company_loan;
   
   
   


    sss = $('#sss').val() || 0;
    sss_provident = $('#sss_provident').val() || 0;
    phic = $('#phic').val() || 0;
    hdmf = $('#hdmf').val() || 0;
    tax_withheld = $('#tax_withheld').val() || 0;
    other_adjustment =  $('#other_adjustment').val() || 0;
    general_loan =  $('#general_loan').val() || 0;
    company_loan =  $('#company_loan').val() || 0;
    
    
    
    let product;
    let product2
    product = (parseFloat(sss) + parseFloat(sss_provident)
                    + parseFloat(phic) + parseFloat(hdmf)
                    + parseFloat(other_adjustment) + parseFloat(tax_withheld)
                    + parseFloat(general_loan) + parseFloat(company_loan)
                    );

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#total_deduction').val(stringNumber);
    $('#total_deduction2').val(product2);
   
    }


// this is for computation of NET PAY

  $(document).ready(function() {
    $('#gross_pay2,#total_deduction2,#adjustment_non_tax').on('input', function() {
       
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
      sss: document.getElementById("sss").value || 0,
      sss_provident_emp: document.getElementById("sss_provident").value || 0,
      phic: document.getElementById("phic").value || 0,
      hdmf: document.getElementById("hdmf").value || 0,
      tax_withheld: document.getElementById("tax_withheld").value || 0,
      other_adjustment: document.getElementById("other_adjustment").value || 0,
      total_deduction: document.getElementById("total_deduction2").value,
      net_pay: document.getElementById("net_pay2").value,
      employee_id_id: document.getElementById("employee_id_id").value,
      general_loan: document.getElementById("general_loan").value || 0,
      company_loan: document.getElementById("company_loan").value || 0,
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
        fieldEmpty()

      }
      return response.json();
  })
  .then(data => {
     
      console.log(data);
      // Do something with the response data
  })
  .catch(error => {
      alert(error)
      console.error('There has been a problem with your fetch operation:', error);
  });
};

document.getElementById("btn_save_payroll_computation").addEventListener("click", savePayrollComputation);

// this funcotion is for emptying the field once the transaction proceed or save
const fieldEmpty = () => {
  document.getElementById("name").value = "";
  // document.getElementById("books").value = "";
  document.getElementById("employee_specs").value = "";
  document.getElementById("basic_pay").value = "";
  document.getElementById("late").value = "";
  document.getElementById("absent").value = "";
  document.getElementById("under_time").value = "";
  document.getElementById("normal_working_day_ot").value = "";
  document.getElementById("spl_30").value = "";
  document.getElementById("legal_holiday").value = "";
  document.getElementById("holiday_ot").value = "";
  document.getElementById("basic_pay_adjustment").value = "";
  document.getElementById("gross_pay").value = "";
  document.getElementById("sss").value = "";
  document.getElementById("sss_provident").value = "";
  document.getElementById("phic").value = "";
  document.getElementById("hdmf").value = "";
  document.getElementById("tax_withheld").value = "";
  document.getElementById("other_adjustment").value = "";
  document.getElementById("total_deduction2").value = "";
  document.getElementById("net_pay").value = "";
  
};
