window.onload = () => {
  const chatBox = document.getElementById("chatBox");
  const input = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const plusBtn = document.getElementById("plusBtn");
  const uploadMenu = document.getElementById("uploadMenu");
  const imageIcon = document.getElementById("imageIcon");
  const docIcon = document.getElementById("docIcon");
  const imageInput = document.getElementById("imageInput");
  const docInput = document.getElementById("docInput");
  const preview = document.getElementById("preview");
  const previewContainer = document.getElementById("previewContainer");
  const voiceBtn = document.getElementById("voiceBtn");

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  // ================= VOICE INPUT =================
  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;

    voiceBtn.onmousedown = () => {
      recognition.start();
      voiceBtn.classList.add("recording");
    };

    voiceBtn.onmouseup = () => {
      recognition.stop();
      voiceBtn.classList.remove("recording");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      input.value = transcript;
      sendBtn.click();
    };

    recognition.onerror = (e) => {
      alert("Voice input error: " + e.error);
    };
  } else {
    voiceBtn.disabled = true;
    alert("Sorry, your browser doesn't support voice input.");
  }

  let attachedImage = null;
  let attachedDoc = null;

  // ================= MENU TOGGLE =================
  plusBtn.onclick = () => {
    uploadMenu.style.display =
      uploadMenu.style.display === "block" ? "none" : "block";
  };

  imageIcon.onclick = () => {
    imageInput.click();
    uploadMenu.style.display = "none";
  };

  docIcon.onclick = () => {
    docInput.click();
    uploadMenu.style.display = "none";
  };

  // ================= IMAGE UPLOAD =================
  imageInput.onchange = () => {
    const file = imageInput.files[0];
    if (!file) return;

    const img = new Image();
    const reader = new FileReader();

    reader.onload = (e) => {
      img.src = e.target.result;
    };

    reader.readAsDataURL(file);

    img.onload = () => {
      const canvas = document.createElement("canvas");
      const maxWidth = 128;
      const scale = (maxWidth < img.width) ? maxWidth / img.width : 1;

      canvas.width = maxWidth;
      canvas.height = img.height * scale;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      canvas.toBlob(
        (blob) => {
          if (!blob || blob.size === 0) {
            alert("⚠️ Image compression failed or blob is empty.");
            return;
          }

          console.log("[✅ Blob ready] Type:", blob.type, "Size:", blob.size);
          attachedImage = blob;

          preview.src = URL.createObjectURL(blob);
          previewContainer.style.display = "flex";

          const infoLine = document.createElement("div");
          infoLine.className = "line";
          infoLine.innerHTML = `<strong>[Image attached: ${file.name}]</strong>`;
          chatBox.appendChild(infoLine);

          chatBox.scrollTop = chatBox.scrollHeight;
        },
        "image/jpeg",
        0.7
      );
    };
  };

  // ================= DOCUMENT UPLOAD =================
  docInput.onchange = () => {
    attachedDoc = docInput.files[0];

    if (attachedDoc) {
      const infoLine = document.createElement("div");
      infoLine.className = "line";
      infoLine.innerHTML = `<strong>[Document attached: ${attachedDoc.name}]</strong>`;
      chatBox.appendChild(infoLine);

      chatBox.scrollTop = chatBox.scrollHeight;
    }
  };

  // ================= SEND BUTTON =================
  sendBtn.onclick = () => {
    const message = input.value.trim();

    if (!message && !attachedImage && !attachedDoc) return;

    // USER MESSAGE
    const userRow = document.createElement("div");
    userRow.className = "messageRow user";

    const userLine = document.createElement("div");
    userLine.className = "bubble userBubble";
    userLine.textContent = message || "[Attachment]";

    userRow.appendChild(userLine);
    chatBox.appendChild(userRow);
    chatBox.scrollTop = chatBox.scrollHeight;

    // BOT MESSAGE CONTAINER
    const botRow = document.createElement("div");
    botRow.className = "messageRow bot";

    const botLine = document.createElement("div");
    botLine.className = "bubble botBubble";

    const liveText = document.createElement("span");
    const liveId = "liveText_" + Date.now();
    liveText.id = liveId;

    botLine.appendChild(liveText);
    botRow.appendChild(botLine);
    chatBox.appendChild(botRow);

    chatBox.scrollTop = chatBox.scrollHeight;

    // FORM DATA
    const formData = new FormData();
    formData.append("message", message);

    if (attachedImage) {
      const file = new File([attachedImage], "compressed.jpg", {
        type: "image/jpeg",
      });
      formData.append("image", file);
    }

    if (attachedDoc) {
      formData.append("document", attachedDoc);
    }

    // RESET INPUTS
    input.value = "";
    preview.src = "";
    previewContainer.style.display = "none";
    imageInput.value = "";
    docInput.value = "";
    attachedImage = null;
    attachedDoc = null;

    startStream(formData, liveId);
  };

  // ================= ENTER KEY SEND =================
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // ================= STREAM FUNCTION (OLD SMOOTH WORKING ONE) =================
  function startStream(formData, liveId) {
    const liveText = document.getElementById(liveId);
    const chatBox = document.getElementById("chatBox");

    fetch("/stream", {
      method: "POST",
      body: formData,
    }).then((response) => {
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      function read() {
        reader.read().then(({ value, done }) => {
          if (done) return;

          const chunk = decoder.decode(value, { stream: true });
          if (chunk === "\0") return;

          liveText.innerHTML += chunk;
          chatBox.scrollTop = chatBox.scrollHeight;

          read();
        });
      }

      read();
    });
  }
};
