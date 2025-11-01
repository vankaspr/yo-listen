import { useEffect, useState } from "react";
import '../../../style/auth/email.css'

export function EmailSentMessage({email}) {
    const [timeLeft, setTimeLeft] = useState(120);
    const [canResend, setCanResend] = useState(false);

    useEffect(() => {
        if (timeLeft > 0) {
            const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
            return () => clearTimeout(timer);
        } else {
            setCanResend(true);
        }
    }, [timeLeft]);

    const formatTime = seconds => {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    };

    const handleResend = async () => {
        // вот здесь нужно написать ручку на беке чтобы запрашивать ещё один токен на имейл
        setTimeLeft(120);
        setCanResend(false);
    };

    return (
        <>
        <div className="email-div">
            <div className="text-email-div">
                
                <h3>Мы отправили вам письмо для подтверждения аккаунта на:</h3>
                <h3><strong>{email}</strong></h3>
            </div>

            
            
            {canResend ? (
                // доработать кнопку 
                <button onClick={handleResend}>Отправить письмо повторно</button>
            ): (
                <div className="timer"><h3>{formatTime(timeLeft)}</h3></div>
            )}
        </div>
        </>
        
    )
}