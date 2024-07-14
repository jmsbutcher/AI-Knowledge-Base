function deleteTriple(triple) {
    fetch("/delete-triple", {
        method: "POST",
        body: JSON.stringify({ triple: triple })
    }).then((_res) => {
        window.location.href = "/knowledge-base";
    });
}

function deleteAdvantage(topic_id, advantage) {
    fetch("/delete-advantage", {
        method: "POST",
        body: JSON.stringify({ topic_id: topic_id, advantage: advantage })
    }).then((_res) => {
        window.location.href = "/topic/" + topic_id;
    });
}


function saveGraph() {
    fetch("/save-graph").then((_res) => {
        window.location.href = "/knowledge-base";
    });
}