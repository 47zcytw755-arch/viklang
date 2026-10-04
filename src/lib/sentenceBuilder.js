const MODEL = 'google/gemini-3.5-flash';

export async function buildSentence(signs) {
  console.log('buildSentence called with signs:', signs);
  
  if (!signs || signs.length === 0) {
    console.log('No signs provided, returning null');
    return null;
  }

  try {
    console.log('About to call OpenRouter API...');
    
    const res = await fetch('/openrouter/api/v1/chat/completions', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 160,
        temperature: 0.3,
        messages: [
          {
            role: 'system',
            content: `You are an ASL-to-English translator in a real-time accessibility app for mute users.
Convert detected ASL sign sequences into natural English sentences.
Rules:
- Single letters are fingerspelling — join into words where they make sense.
- Phrases like Hello/Yes/No/Thank you are complete units.
- Output ONLY the final English sentence. No explanation, no quotes.
- If it's just one letter: "Letter [X]"`
          },
          {
            role: 'user',
            content: `Signs: ${signs.join(' ')}\nTranslate:`
          }
        ]
      })
    });

    console.log('API Response status:', res.status);
    
    if (!res.ok) {
      console.error('API Error:', res.status, res.statusText);
      const errorText = await res.text();
      console.error('Error details:', errorText);
      return null;
    }
    
    const data = await res.json();
    console.log('API Response data:', data);
    const result = data.choices?.[0]?.message?.content?.trim() || null;
    console.log('Final result:', result);
    return result;
  } catch (err) {
    console.error('sentenceBuilder error:', err);
    return null;
  }
}
