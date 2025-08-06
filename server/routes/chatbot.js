const express = require('express');
const { Configuration, OpenAIApi } = require('openai');
const router = express.Router();

// Initialize OpenAI (if API key is provided)
let openai = null;
if (process.env.OPENAI_API_KEY) {
  const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  });
  openai = new OpenAIApi(configuration);
}

// Error checking rules and patterns
const errorCheckingRules = [
  {
    id: 'missing-safety',
    pattern: /(?!.*(?:safety|ppe|protective|lockout|tagout|emergency))/i,
    message: 'Consider adding safety precautions or PPE requirements',
    severity: 'warning',
    category: 'safety'
  },
  {
    id: 'unclear-steps',
    pattern: /\b(?:maybe|perhaps|might|could|should probably)\b/i,
    message: 'Avoid uncertain language in instructions. Use clear, definitive statements.',
    severity: 'error',
    category: 'clarity'
  },
  {
    id: 'missing-tools',
    pattern: /(?=.*(?:using|use|with))(?!.*(?:tool|equipment|instrument))/i,
    message: 'Specify the tools or equipment required for this step',
    severity: 'warning',
    category: 'tools'
  },
  {
    id: 'passive-voice',
    pattern: /\b(?:is|was|were|been|being)\s+\w+ed\b/i,
    message: 'Consider using active voice for clearer instructions',
    severity: 'info',
    category: 'style'
  },
  {
    id: 'missing-verification',
    pattern: /(?=.*(?:install|connect|attach|mount))(?!.*(?:verify|check|ensure|confirm))/i,
    message: 'Add verification step to confirm proper installation/connection',
    severity: 'warning',
    category: 'quality'
  }
];

// Check content for errors
router.post('/check', async (req, res) => {
  try {
    const { content, type = 'text' } = req.body;
    
    if (!content || typeof content !== 'string') {
      return res.status(400).json({ error: 'Content is required' });
    }
    
    const issues = [];
    
    // Apply rule-based checking
    for (const rule of errorCheckingRules) {
      if (rule.pattern.test(content)) {
        issues.push({
          id: rule.id,
          message: rule.message,
          severity: rule.severity,
          category: rule.category,
          line: findLineNumber(content, rule.pattern)
        });
      }
    }
    
    // Additional checks based on content type
    if (type === 'procedure') {
      issues.push(...checkProcedureSpecific(content));
    } else if (type === 'safety') {
      issues.push(...checkSafetySpecific(content));
    }
    
    // AI-powered checking (if OpenAI is available)
    let aiSuggestions = [];
    if (openai) {
      try {
        aiSuggestions = await getAISuggestions(content, type);
      } catch (error) {
        console.warn('AI suggestions unavailable:', error.message);
      }
    }
    
    res.json({
      issues,
      aiSuggestions,
      summary: {
        totalIssues: issues.length,
        errors: issues.filter(i => i.severity === 'error').length,
        warnings: issues.filter(i => i.severity === 'warning').length,
        info: issues.filter(i => i.severity === 'info').length
      }
    });
  } catch (error) {
    console.error('Error checking content:', error);
    res.status(500).json({ error: 'Failed to check content' });
  }
});

// Get AI suggestions for improvement
router.post('/suggestions', async (req, res) => {
  try {
    const { content, context = 'general' } = req.body;
    
    if (!content || typeof content !== 'string') {
      return res.status(400).json({ error: 'Content is required' });
    }
    
    if (!openai) {
      return res.status(503).json({ error: 'AI service not available. Please configure OpenAI API key.' });
    }
    
    const suggestions = await getAISuggestions(content, context);
    res.json({ suggestions });
  } catch (error) {
    console.error('Error getting AI suggestions:', error);
    res.status(500).json({ error: 'Failed to get AI suggestions' });
  }
});

// Chat with AI assistant
router.post('/chat', async (req, res) => {
  try {
    const { message, context = '', history = [] } = req.body;
    
    if (!message || typeof message !== 'string') {
      return res.status(400).json({ error: 'Message is required' });
    }
    
    if (!openai) {
      return res.status(503).json({ 
        error: 'AI chat not available. Please configure OpenAI API key.',
        fallbackResponse: getFallbackResponse(message)
      });
    }
    
    const systemPrompt = `You are an expert assistant for work instruction creation. You help users write clear, safe, and effective work instructions. Focus on:
    - Safety considerations and PPE requirements
    - Clear, actionable steps
    - Quality control measures
    - Proper tool and equipment specification
    - Compliance with industry standards
    
    Current context: ${context}`;
    
    const messages = [
      { role: 'system', content: systemPrompt },
      ...history.slice(-10), // Keep last 10 messages for context
      { role: 'user', content: message }
    ];
    
    const response = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      messages,
      max_tokens: 500,
      temperature: 0.7
    });
    
    const aiResponse = response.data.choices[0].message.content;
    
    res.json({
      response: aiResponse,
      suggestions: extractSuggestions(aiResponse)
    });
  } catch (error) {
    console.error('Error in AI chat:', error);
    res.status(500).json({ 
      error: 'Failed to process chat message',
      fallbackResponse: getFallbackResponse(req.body.message)
    });
  }
});

// Helper functions
function findLineNumber(content, pattern) {
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (pattern.test(lines[i])) {
      return i + 1;
    }
  }
  return null;
}

function checkProcedureSpecific(content) {
  const issues = [];
  
  // Check for numbered steps
  if (!/^\s*\d+\./m.test(content)) {
    issues.push({
      id: 'missing-numbered-steps',
      message: 'Consider using numbered steps for procedures',
      severity: 'info',
      category: 'structure'
    });
  }
  
  // Check for prerequisite section
  if (!/prerequisite|requirement|before|prior/i.test(content)) {
    issues.push({
      id: 'missing-prerequisites',
      message: 'Consider adding prerequisites or requirements section',
      severity: 'warning',
      category: 'structure'
    });
  }
  
  return issues;
}

function checkSafetySpecific(content) {
  const issues = [];
  
  // Check for PPE mentions
  if (!/ppe|personal protective equipment|safety glasses|gloves|helmet/i.test(content)) {
    issues.push({
      id: 'missing-ppe',
      message: 'Consider specifying required Personal Protective Equipment (PPE)',
      severity: 'error',
      category: 'safety'
    });
  }
  
  // Check for emergency procedures
  if (!/emergency|accident|incident|injury/i.test(content)) {
    issues.push({
      id: 'missing-emergency',
      message: 'Consider adding emergency procedure information',
      severity: 'warning',
      category: 'safety'
    });
  }
  
  return issues;
}

async function getAISuggestions(content, context) {
  if (!openai) return [];
  
  const prompt = `Analyze the following work instruction content and provide 3-5 specific suggestions for improvement. Focus on safety, clarity, and completeness.

Context: ${context}
Content: ${content}

Provide suggestions in JSON format with fields: type, message, priority (high/medium/low)`;
  
  try {
    const response = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 400,
      temperature: 0.3
    });
    
    const aiResponse = response.data.choices[0].message.content;
    return JSON.parse(aiResponse);
  } catch (error) {
    console.warn('Failed to parse AI suggestions:', error);
    return [];
  }
}

function getFallbackResponse(message) {
  const responses = {
    safety: "Always prioritize safety in work instructions. Consider adding PPE requirements and emergency procedures.",
    tools: "Make sure to specify all required tools and equipment with proper specifications.",
    steps: "Use clear, numbered steps with active voice. Each step should be specific and actionable.",
    quality: "Include quality control checkpoints and verification steps throughout the procedure."
  };
  
  const lowerMessage = message.toLowerCase();
  
  for (const [key, response] of Object.entries(responses)) {
    if (lowerMessage.includes(key)) {
      return response;
    }
  }
  
  return "I can help you improve your work instructions. Consider focusing on safety, clarity, and completeness.";
}

function extractSuggestions(aiResponse) {
  // Simple extraction of actionable suggestions from AI response
  const suggestions = [];
  const lines = aiResponse.split('\n');
  
  lines.forEach(line => {
    if (line.includes('consider') || line.includes('add') || line.includes('include')) {
      suggestions.push({
        type: 'improvement',
        message: line.trim(),
        priority: 'medium'
      });
    }
  });
  
  return suggestions.slice(0, 3); // Return top 3 suggestions
}

module.exports = router;