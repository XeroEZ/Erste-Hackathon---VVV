from . import geminiKey


def OtazkaNaGeminiBasic(otazka) -> str:

    try:
        client = geminiKey.ClientApi()
        

        prompt_text = ({otazka}
        )

        config = geminiKey.types.GenerateContentConfig(
            temperature=0.0
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt_text,
            config=config,
        )
        return response.text.strip()

    except Exception as e:
        return f"Nastala chyba pri volaní AI: {e}"



def main():
    print("Vitaj v komunikacije s Gemini")
    # spýtaj sa používateľa na odpoveď
    user_input = input("Zadaj svoju otazku?")
    # volanie tvojej funkcie AkinatorHra s parametrom
    result = AkinatorHra(user_input)
    # vypíš výsledok
    print("Výsledok:", result)


if __name__ == "__main__":
    main()
