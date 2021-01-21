window.myNamespace = Object.assign({}, window.myNamespace, {
    tabulator: {
        cellLog: function (e, cell, table) {
            console.log("Cell got")
            console.log(e)
            console.log(cell)
        }
    }
});