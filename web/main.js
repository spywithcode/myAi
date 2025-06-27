$(document).ready(() => {
    // Initialize animated text
    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" }
    });

    // Initialize SiriWave animation
    const siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: 1,
        speed: 0.30,
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp", sync: true },
        out: { effect: "fadeOutUp", sync: true }
    });

    // Utility: Toggle visibility of mic and send buttons
    const toggleButtonVisibility = (message) => {
        const showMic = message.length === 0;
        $("#MicBtn").attr('hidden', !showMic);
        $("#SendBtn").attr('hidden', showMic);
    };

    // Utility: Handle assistant play logic
    const playAssistant = (message) => {
        if (!message) return;
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands(message);
        $("#chatbox").val("");
        toggleButtonVisibility("");
    };

    // Event: Mic button click
    $("#MicBtn").on("click", () => {
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();
    });

    // Event: Keyboard shortcut (Ctrl/Cmd + J)
    $(document).on("keyup", (e) => {
        if (e.key === 'j' && (e.ctrlKey || e.metaKey)) {
            eel.playAssistantSound();
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()();
        }
    });

    // Event: Chatbox input change
    $("#chatbox").on("keyup", () => {
        const message = $("#chatbox").val();
        toggleButtonVisibility(message);
    });

    // Event: Send button click
    $("#SendBtn").on("click", () => {
        const message = $("#chatbox").val();
        playAssistant(message);
    });

    // Event: Enter key in chatbox
    $("#chatbox").on("keypress", (e) => {
        if (e.which === 13) {
            const message = $("#chatbox").val();
            playAssistant(message);
        }
    });

    // Python se message lekar .siri-message mein dikhana
    eel.get_assistant_message()((message) => {
        $('.siri-message').text(message);
        // Optional: Animate again if needed
        $('.siri-message').textillate('in');
    });
});
