// $(document).ready(function(){
//     $('#btn_search').click(function(){
//         var datefrom = $('#datefrom').val();
//         var dateto = $('#dateto').val();

//         $.ajax({
//             type: 'POST',
//             url: '/graphql', // Change this to your GraphQL endpoint
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 query: `query MyQuery {
//                     getMonthlyPayrollReportTest(datefrom: "${datefrom}", dateto: "${dateto}") {
//                         name
//                         book
//                         totalGrossPay
//                         netPay
//                         allowance
//                         AllowanceMeals
//                         developmental
//                         allowanceDeduction
//                         totalSss
//                         phic
//                         hdmf
//                         totalNonTaxableIncome
//                         netPayAfterNonTax
//                     }
//                 }`
//             }),
//             success: function(response) {
//                 var data = response.data.getMonthlyPayrollReportTest;
//                 var tbody = $('#table_payroll_monthly_report2');
//                 tbody.empty();
//                 console.log(data);
//                 $.each(data, function(index, item){
//                     var row = $('<tr>');
//                     row.append($('<td>').text(item.name));
//                     row.append($('<td>').text(item.book));
                  
//                     row.append($('<td>').text(item.totalGrossPay));
//                     row.append($('<td>').text(formatNumber(item.totalSss)));
//                     row.append($('<td>').text(formatNumber(item.phic)));
//                     row.append($('<td>').text(formatNumber(item.hdmf)));
//                     row.append($('<td>').text(formatNumber(item.netPay)));
//                     row.append($('<td>').text(formatNumber(item.allowance)));
//                     row.append($('<td>').text(formatNumber(item.AllowanceMeals)));
//                     row.append($('<td>').text(formatNumber(item.developmental)));
//                     row.append($('<td>').text(formatNumber(item.allowanceDeduction)));
//                     row.append($('<td>').text(formatNumber(item.totalNonTaxableIncome)));
//                     row.append($('<td>').text(formatNumber(item.netPayAfterNonTax)));
//                     tbody.append(row);
//                 });
//                 initializeDataTable();
//             },
//             error: function(xhr, status, error) {
//                 console.error('Error:', error);
//             }
//         });
//     });
// });

// // Function to initialize DataTable
// const initializeDataTable = () => {
//     $('#table_payroll_monthly_report').DataTable({
//         dom: 'Bfrtip',
//         buttons: [
//             { // EXCEL
//                 extend : 'excel',
//                 text: 'Export Excel',
//                 className: 'btn btn-success',
//                 titleArttr: 'Excel',
//                 exportOptions: {
//                     columns: [0,1,2,3,4,5,6,7,8,9,10,
//                         11,12,13,14,15,16,17
//                     ]
//                 },
//             },
//         ]
//     });
// };

// const initializeDataTable = () => {
//     $('#table_payroll_monthly_report').DataTable({
//         buttons: [
//             'excel'
//         ]
//     });
// };

$(document).ready(function() {
    $('#btn_search').click(function() {
        var datefrom = $('#datefrom').val();
        var dateto = $('#dateto').val();

        $.ajax({
            type: 'POST',
            url: '/graphql', // Change this to your GraphQL endpoint
            contentType: 'application/json',
            data: JSON.stringify({
                query: `query MyQuery {
                    getMonthlyPayrollReportWithSss(datefrom: "${datefrom}", dateto: "${dateto}") {
                        name
                        book
                        totalGrossPay
                        totalSss
                        phic
                        hdmf
                        netPay
                        allowance
                        AllowanceMeals
                        developmental
                        allowanceDeduction
                        totalNonTaxableIncome
                        netPayAfterNonTax
                        sssEmployerShare
                        ecc
                        phicEmployer
                        hdmfEmploye
                        TaxWithheld
                    }
                }`
            }),
            success: function(response) {
                var data = response.data.getMonthlyPayrollReportWithSss;
                var tableBody = $('#table_payroll_monthly_report2');
                tableBody.empty();

                data.forEach(function(item) {
                    var formattedGrossPayAmount = parseFloat(item.totalGrossPay).toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                    var row = '<tr>' +
                        '<td>' + item.name + '</td>' +
                        '<td>' + item.book + '</td>' +
                        '<td>' + formatNumber(item.totalGrossPay) + '</td>' +
                        '<td>' + formatNumber(item.totalSss) + '</td>' +
                        '<td>' + formatNumber(item.sssEmployerShare) + '</td>' +
                        '<td>' + formatNumber(item.ecc) + '</td>' +
                        '<td>' + formatNumber(item.phic) + '</td>' +
                        '<td>' + formatNumber(item.phicEmployer) + '</td>' +
                        '<td>' + formatNumber(item.hdmf) + '</td>' +
                        '<td>' + formatNumber(item.hdmfEmploye) + '</td>' +
                        '<td>' + formatNumber(item.TaxWithheld) + '</td>' +
                        '<td>' + formatNumber(item.netPay) + '</td>' +
                        '<td>' + formatNumber(item.allowance) + '</td>' +
                        '<td>' + formatNumber(item.AllowanceMeals) + '</td>' +
                        '<td>' + formatNumber(item.developmental) + '</td>' +
                        '<td>' + formatNumber(item.allowanceDeduction) + '</td>' +
                        '<td>' + formatNumber(item.totalNonTaxableIncome) + '</td>' +
                        '<td>' + formatNumber(item.netPayAfterNonTax) + '</td>'
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

function payrollListExcel(type){
    var data = document.getElementById('table_payroll_monthly_report');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'payroll_list.' + type);

}




