document.addEventListener("DOMContentLoaded", () => {
const form = document.querySelector("form");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    try {

        const formData = new FormData(form);

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        let html = `
        <div class="result-card">
            <h2>🏆 Best Candidate</h2>
            <h3>${data.best_candidate.filename}</h3>
            <p>Match: ${data.best_candidate.percentage}%</p>

            <br>

            <p>
                ✅ Matched Skills:
                ${data.best_candidate.matched_words.join(", ") || "None"}
            </p>

            <br>

            <p>
                ❌ Missing Skills:
                ${data.best_candidate.missing_words.join(", ") || "None"}
            </p>
        </div>
        `;

        html += `
        <div class="table-box">
            <table>

                <tr>
                    <th>Rank</th>
                    <th>Resume</th>
                    <th>Match %</th>
                </tr>
        `;

        data.ranking.forEach((item, index) => {

            html += `
            <tr>
                <td>${index + 1}</td>
                <td>${item.filename}</td>
                <td>${item.percentage}%</td>
            </tr>
            `;
        });

        html += `
            </table>
        </div>
        `;

        document.getElementById("results").innerHTML = html;

    } catch (error) {

        console.error(error);
        alert("Error aaya. F12 Console dekho.");
    }
});
});
