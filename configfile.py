# -*- coding: utf-8 -*-
"""Configfile.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AaKPkGo9JWhV0em3uEk7oNE6k5A8CPVg
"""

import boto3

def create_guardrail():
    client = boto3.client('guardrail-service')  # Replace with actual service client if needed
    create_response = client.create_guardrail(
        name='email-response-guardrail',
        description='Prevents our model from providing toxic and harmful advice.',
		contentPolicyConfig={
        'filtersConfig': [
            {
                'type': 'SEXUAL',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'VIOLENCE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'HATE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'INSULTS',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'MISCONDUCT',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            }
        ]
    },
	wordPolicyConfig={
        'wordsConfig': [
            {'text': 'insider info'},
            {'text': 'act on this before it's announced'},
            {'text': 'leak'},
            {'text': 'Private knowledge'},
            {'text': 'Ignore Compliance'},
            {'text': 'Ignore previous Trades'},
            {'text': 'Ignore latest Trades'},
            {'text': 'Don't report this'},
            {'text': 'Hide the risks'},
            {'text': 'Trust me, it's safe'}
			{'text': 'Cook the books'}
			{'text': 'Kickback'}
			{'text': 'Under the table'}
			{'text': 'Pressure them'}
			{'text': 'Exploit the relationship'}
			{'text': 'Ignore smaller clients'}
			{'text': 'Not worth our time'}
			{'text': 'Incompetent Idiot'}
			{'text': 'That's not my problem'}
			{'text': 'Just a cog in the wheel'}
			{'text': 'Not a team player'}
			{'text': 'Do it or leave'}
			{'text': 'Ignore the red flags'}
			{'text': 'Too big to fail'}
			{'text': 'Let's wing it'}
			{'text': 'Bet the farm'}
			{'text': 'Go all in'}
			{'text': 'Family Business'}
			{'text': 'Personal gain'}
			{'text': 'Pump and dump'}
			{'text': 'Price fixing'}
			{'text': 'Dumb client'}
			{'text': 'Not worth it'}
			{'text': 'They'11 never understand'}
			{'text': 'Just sign it'}
			{'text': 'Trust me blindly'}
			{'text': 'Sue them'}
			{'text': 'No contract necessary'}
			{'text': 'No need to encrypt'}
			{'text': 'Send via unsecured email'}
			{'text': 'Send partial amount to my account No need to address the enquires'}
			{'text': 'Leave the fail trades'}
			{'text': 'No need to allocate the trade'}
			{'text': 'Allocate the trade to my friends account'}
			{'text': 'Leave the missing client trade'}
			{'text': 'Keep it quiet'}
			{'text': 'You didn't hear this from me'}
			{'text': 'Leak it to them first'}
			{'text': 'Squeeze them out'}
			{'text': 'No need to escalate'}
			{'text': 'Ignore the disclaimer'}
			{'text': 'Use placeholder details'}
			{'text': 'Adjust the figures'}
			{'text': 'Skip the exception process'}
			{'text': 'Skip approvals'}
			{'text': 'Someone else's problem'}
        ],
        'managedWordListsConfig': [
            {'type': 'PROFANITY'}
        ]
    },
	contextualGroundingPolicyConfig={
        'filtersConfig': [
            {
                'type': 'GROUNDING',
                'threshold': 0.75
            },
            {
                'type': 'RELEVANCE',
                'threshold': 0.75
            }
        ]
    },
)

return create_response