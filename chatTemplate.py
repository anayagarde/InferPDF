css = '''
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #0f1117;
    color: #f1f5f9;
}

.chat-msg {
    display: flex;
    align-items: center;  /* align vertically */
    gap: 1rem;
    padding: 1rem 1.25rem;
    border-radius: 1.25rem;
    margin-bottom: 1.5rem;
    max-width: 85%;
    min-height: 70px;  /* <-- ensure enough space for avatar */
    position: relative;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    backdrop-filter: blur(6px);
}


.chat-msg.user {
    background: #1c1e26;
    margin-left: auto;
    border-right: 6px solid #f39c12;
    flex-direction: row-reverse;
}

.chat-msg.bot {
    background: linear-gradient(145deg, #2e3548, #3a4157);
    border-left: 6px solid #7289da;
}

.chat-msg .avatar {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-msg .avatar img {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #fff;
    box-shadow: 0 0 6px rgba(255,255,255,0.1);
}

.chat-msg .message {
    flex: 1;
    font-size: 1rem;
    line-height: 1.6;
    word-break: break-word;
    white-space: pre-wrap;
    padding-right: 1.5rem;
}

.chat-msg .timestamp {
    position: absolute;
    bottom: 8px;
    right: 16px;
    font-size: 0.72rem;
    color: #cbd5e1;
    opacity: 0.7;
}

/* Optional typing animation */
.typing-dots {
    display: flex;
    gap: 6px;
    margin-top: 6px;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    background-color: #bbb;
    border-radius: 50%;
    animation: blink 1.4s infinite both;
}

.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}
.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes blink {
    0%, 80%, 100% { opacity: 0; }
    40% { opacity: 1; }
}
</style>
'''


from datetime import datetime

current_time = datetime.now().strftime("%I:%M %p")

bot_template = f'''
<div class="chat-msg bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" alt="Bot">
    </div>
    <div class="message">{{{{MSG}}}}</div>
    <div class="timestamp">{current_time}</div>
</div>
'''

user_template = f'''
<div class="chat-msg user">
    <div class="message">{{{{MSG}}}}</div>
    <div class="timestamp">{datetime.now().strftime("%I:%M %p")}</div>
</div>
'''



typing_template = '''
<div class="chat-msg bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" alt="Bot">
    </div>
    <div class="message">
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
    </div>
</div>
'''
