function generatePDF(){
    const element = document.getElementById("results");

    html2pdf()
    .from(element)
    .save();
}