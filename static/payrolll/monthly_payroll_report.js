$(document).ready(function(){
    $('#btn_search').click(function(){
        var datefrom = $('#datefrom').val();
        var dateto = $('#dateto').val();

        $.ajax({
            type: 'POST',
            url: '/graphql', // Change this to your GraphQL endpoint
            contentType: 'application/json',
            data: JSON.stringify({
                query: `query MyQuery {
                    getMonthlyPayrollReportTest(datefrom: "${datefrom}", dateto: "${dateto}") {
                        name
                        book
                        totalGrossPay
                        netPay
                        allowance
                        AllowanceMeals
                        developmental
                        allowanceDeduction
                        totalSss
                        phic
                        hdmf
                        totalNonTaxableIncome
                        netPayAfterNonTax
                    }
                }`
            }),
            success: function(response) {
                var data = response.data.getMonthlyPayrollReportTest;
                var tbody = $('#table_payroll_monthly_report2');
                tbody.empty();
                console.log(data);
                $.each(data, function(index, item){
                    var row = $('<tr>');
                    row.append($('<td>').text(item.name));
                    row.append($('<td>').text(item.book));
                  
                    row.append($('<td>').text(formatNumber(item.totalGrossPay)));
                    row.append($('<td>').text(formatNumber(item.totalSss)));
                    row.append($('<td>').text(formatNumber(item.phic)));
                    row.append($('<td>').text(formatNumber(item.hdmf)));
                    row.append($('<td>').text(formatNumber(item.netPay)));
                    row.append($('<td>').text(formatNumber(item.allowance)));
                    row.append($('<td>').text(formatNumber(item.AllowanceMeals)));
                    row.append($('<td>').text(formatNumber(item.developmental)));
                    row.append($('<td>').text(formatNumber(item.allowanceDeduction)));
                    row.append($('<td>').text(formatNumber(item.totalNonTaxableIncome)));
                    row.append($('<td>').text(formatNumber(item.netPayAfterNonTax)));
                    tbody.append(row);
                });
                initializeDataTable();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});

const initializeDataTable = () => {
    $('#table_payroll_monthly_report').DataTable();
};


function formatNumber(number) {
    // Check if the number is valid
    if (isNaN(number)) {
        return number; // Return as is if not a valid numbergit add 
    }
    
    // Format number with thousand separator and 2 decimal places
    return parseFloat(number).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// function payrollListExcel(type){
//     var data = document.getElementById('table_payroll_monthly_report2');
//     var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
//     XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
//     XLSX.writeFile(file, 'payroll_list.' + type);

// }


// function payrollListExcel(type){
//     // Get the table element
//     var data = document.getElementById('table_payroll_monthly_report2');
    
//     // Extract column names
//     var columns = [];
//     var headers = data.getElementsByTagName('th');
//     for (var i = 0; i < headers.length; i++) {
//         columns.push(headers[i].textContent);
//     }

//     // Convert table data to workbook
//     var tableData = XLSX.utils.table_to_sheet(data);

//     // Add column names to the workbook
//     XLSX.utils.sheet_add_aoa(tableData, [columns], {origin: -1});

//     // Create a workbook
//     var file = XLSX.utils.book_new();
//     XLSX.utils.book_append_sheet(file, tableData, 'Sheet1');

//     // Write and save the workbook
//     var wbout = XLSX.write(file, {bookType: type, bookSST: true, type: 'binary'});
//     function s2ab(s) {
//         var buf = new ArrayBuffer(s.length);
//         var view = new Uint8Array(buf);
//         for (var i=0; i<s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
//         return buf;
//     }
//     saveAs(new Blob([s2ab(wbout)],{type:"application/octet-stream"}), 'payroll_list.' + type);
// }
// function payrollListExcel(type) {
//     var data = document.getElementById('table_payroll_monthly_report2');

//     // Extract column names
//     var columns = [];
//     $('#table_payroll_monthly_report thead').each(function() {
//         columns.push($(this).text());
//     });

//     // Extract data from table rows
//     var tableData = [];
//     $('#table_payroll_monthly_report2 tr').each(function() {
//         var rowData = [];
//         $(this).find('td').each(function() {
//             rowData.push($(this).text());
//         });
//         tableData.push(rowData);
//     });

//     // Create a workbook
//     var wb = XLSX.utils.book_new();

//     // Convert data to worksheet
//     var sheet = XLSX.utils.aoa_to_sheet([columns]); // Add column headers
//     XLSX.utils.sheet_add_aoa(sheet, tableData, { origin: 'A2' }); // Add table data below headers

//     // Append worksheet to the workbook
//     XLSX.utils.book_append_sheet(wb, sheet, 'Sheet1');

//     // Save workbook
//     XLSX.writeFile(wb, 'payroll_list.' + type);
// }

function payrollListExcel(type) {
    var data = document.getElementById('table_payroll_monthly_report2');

    // Define clean column headers
    var cleanColumnHeaders = ['Name', 'Books', 'Gross Pay', 'SSS', 'PHIC', 
                                'HDMF', 'Net Pay', 'Allowance', 'Meal Allowance',
                                 'Developmental', 'Allowance Deduction','Total Non-Tax','Net After Non Tax'];

    // Extract data from table rows
    var tableData = [];
    $('#table_payroll_monthly_report2 tr').each(function() {
        var rowData = [];
        $(this).find('td').each(function() {
            rowData.push($(this).text());
        });
        tableData.push(rowData);
    });

    // Create a workbook
    var wb = XLSX.utils.book_new();

    // Convert data to worksheet
    var sheet = XLSX.utils.aoa_to_sheet([cleanColumnHeaders]); // Use clean column headers
    XLSX.utils.sheet_add_aoa(sheet, tableData, { origin: 'A2' }); // Add table data below headers

    // Append worksheet to the workbook
    XLSX.utils.book_append_sheet(wb, sheet, 'Sheet1');

    // Save workbook
    XLSX.writeFile(wb, 'payroll_list.' + type);
}








