const previewInfo = document.getElementById("preview-info");
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file");
const uploadBtn = document.getElementById("upload");
const previewList = document.getElementById("preview-list");
const progressBar = document.getElementById("progress-bar");
const progressPercent = document.getElementById("progress-percent");
const progressStatus = document.getElementById("progress-status");


let selectedFiles = [];
// ======================
// Upload
// ======================

uploadBtn.onclick = () => {

    if (fileInput.files.length === 0) {

        showToast("📂 กรุณาเลือกไฟล์");

        return;

    }

    const formData = new FormData();

    for (const file of selectedFiles) {

        formData.append("file", file);

    }

    

    progressBar.style.width = "0%";
    progressPercent.textContent = "0%";
    progressStatus.textContent = "Uploading...";

    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = (e) => {

        if (e.lengthComputable) {

            const percent = Math.round(
                (e.loaded / e.total) * 100
            );

            progressBar.style.width = percent + "%";
            progressPercent.textContent = percent + "%";

        }

    };

    xhr.onload = () => {

        progressBar.style.width = "100%";
        progressPercent.textContent = "100%";
        progressStatus.textContent = "Upload Complete";

        let data = JSON.parse(xhr.responseText);


            if (!Array.isArray(data)) {

                data = [data];

            }

            

            data.forEach(item => {

                const card = document.querySelector(
                    `[data-original="${item.original_name}"]`
                );

                if (!card) return;

                const status =
                    card.querySelector(".upload-status");

                const actions =
                    card.querySelector(".upload-actions");

                if(item.success){

                    status.innerHTML = "✅ Upload Success";

                    actions.innerHTML = `

                        <button
                            onclick="copyLink('${item.url}')">

                            📋 Copy Link

                        </button>

                        <button
                            onclick="window.open('${item.url}','_blank')">

                            🌐 Open File

                        </button>

                    `;

                }else{

                    status.innerHTML =
                        "❌ Upload Failed";

                }

        });

                showToast("✅ Upload สำเร็จ");

            };


            xhr.open(
                "POST",
                "/upload"
            );

            xhr.send(formData);

        };

// ======================
// Drag & Drop
// ======================

        ["dragenter", "dragover"].forEach(eventName => {

            dropArea.addEventListener(eventName, e => {

                e.preventDefault();

                dropArea.classList.add("drag");

            });

        });

["dragleave", "drop"].forEach(eventName => {

    dropArea.addEventListener(eventName, e => {

        e.preventDefault();

        dropArea.classList.remove("drag");

    });

});

dropArea.addEventListener("drop", e => {

    e.preventDefault();

    const dt = new DataTransfer();

    for (const file of e.dataTransfer.files) {

        dt.items.add(file);

    }

    fileInput.files = dt.files;
    showPreview(fileInput.files);

});

// ======================
// Click Drop Area
// ======================

dropArea.onclick = () => {

    fileInput.click();

};

fileInput.addEventListener("change", () => {

    showPreview(fileInput.files);

});

// ======================
// Copy Link
// ======================

function copyLink(url) {

    if (navigator.clipboard && window.isSecureContext) {

        navigator.clipboard.writeText(url)
            .then(() => {

                showToast("📋 คัดลอกลิงก์แล้ว");

            })
            .catch(() => {

                fallbackCopy(url);

            });

    } else {

        fallbackCopy(url);

    }

}

// ======================
// Fallback Copy
// ======================

function fallbackCopy(text) {

    const textarea = document.createElement("textarea");

    textarea.value = text;

    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";

    document.body.appendChild(textarea);

    textarea.focus();

    textarea.select();

    try {

        document.execCommand("copy");

        showToast("📋 คัดลอกลิงก์แล้ว");

    } catch (err) {

        showToast("❌ ไม่สามารถคัดลอกลิงก์ได้");

    }

    document.body.removeChild(textarea);

}

// ======================
// Toast
// ======================

function showToast(message) {

    const toast = document.getElementById("toast");

    if (!toast) {

        return;

    }

    toast.innerHTML = message;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 2000);

}

function showPreview(files){

    selectedFiles = [...files];

    previewList.innerHTML = "";

    let totalSize = 0;

    selectedFiles.forEach((file,index)=>{

        totalSize += file.size;

        const card = document.createElement("div");

        card.className = "preview-card";

        card.dataset.original = file.name;

        if(file.type.startsWith("image/")){

            const img = document.createElement("img");

            img.src = URL.createObjectURL(file);

            img.className = "preview-image";

            card.appendChild(img);

        }else{

            card.insertAdjacentHTML("beforeend",`
                <div class="file-icon">
                    📄
                </div>
            `);



        }

        

        card.insertAdjacentHTML("beforeend", `

            <button
                class="remove-file"
                onclick="removeFile(${index})">

                ✕

            </button>

            <div class="preview-name">
                ${file.name}
            </div>

            <div class="preview-size">
                ${(file.size / 1024 / 1024).toFixed(2)} MB
            </div>

            <div class="upload-status">
                ⏳ รออัปโหลด
            </div>

            <div class="upload-actions"></div>

        `);

                previewList.appendChild(card);

            });

    previewInfo.innerHTML = `
        เลือกแล้ว ${selectedFiles.length} ไฟล์
        (${(totalSize/1024/1024).toFixed(2)} MB)
    `;

    }

function removeFile(index){

    selectedFiles.splice(index,1);

    const dt = new DataTransfer();

    selectedFiles.forEach(file=>{

        dt.items.add(file);

    });

    fileInput.files = dt.files;

    showPreview(fileInput.files);

}