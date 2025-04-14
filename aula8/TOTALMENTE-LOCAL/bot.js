const { Client, LocalAuth } = require("whatsapp-web.js");
const axios = require("axios");
const qrcode = require("qrcode-terminal");

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on("qr", (qr) => {
    console.log("📱 Escaneie o QR Code para conectar seu bot ao WhatsApp:");
    qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
    console.log("✅ Bot do WhatsApp está pronto!");
});

client.on("message", async (message) => {
    if (message.isGroupMsg) return;
    console.log(`📩 Mensagem recebida: ${message.body}`);

    if (!message.body) return;

    try {
        const response = await axios.post("http://localhost:3000/chat", {
            prompt: message.body
        });

        const botResponse = response.data.response.replace(/<\/?[^>]+(>|$)/g, "");
        await message.reply(botResponse);
        console.log(`🤖 Resposta enviada: ${botResponse}`);
    } catch (error) {
        console.error("❌ Erro ao processar a mensagem:", error.message);
        await message.reply("⚠️ Ocorreu um erro ao processar sua mensagem.");
    }
});

client.initialize();
