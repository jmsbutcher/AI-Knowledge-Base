function deleteTriple(triple) {
    fetch("/delete-triple", {
        method: "POST",
        body: JSON.stringify({ triple: triple })
    }).then((_res) => {
        window.location.href = "/knowledge-base";
    });
}

function saveGraph() {
    fetch("/save-graph").then((_res) => {
        window.location.href = "/knowledge-base";
    });
}