import { View, Text, Image, ScrollView, TouchableOpacity } from "react-native";
import React, { useState, useEffect, useRef } from "react";
import { useLocalSearchParams, router } from "expo-router";
import { images } from "@/constants/images";
import { icons } from "@/constants/icons";
import SearchBar from "@/components/SearchBar";
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

const Chat = () => {
  const { id, prompt } = useLocalSearchParams<{ id: string; prompt?: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollViewRef = useRef<ScrollView>(null);

  /**
   * Send message to AI backend using the same approach as signin
   */
  const sendMessageToAI = async (userMessage: string) => {
    try {
      const apiUrl = `${process.env.EXPO_PUBLIC_API_URL}api/chat/message/`;
      console.log("Chat API URL:", apiUrl);
      console.log("Environment variable:", process.env.EXPO_PUBLIC_API_URL);
      console.log("Full URL being called:", apiUrl);

      // Create abort controller for timeout functionality
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout for AI

      console.log("Sending request to:", apiUrl);
      console.log(
        "Request body:",
        JSON.stringify({
          message: userMessage,
          chat_id: id,
        })
      );

      const response = await fetch(
        `${process.env.EXPO_PUBLIC_API_URL}api/chat/message/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userMessage,
            chat_id: id,
          }),
          signal: controller.signal, // For timeout functionality
        }
      );

      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);

      // Clear the timeout since request completed
      clearTimeout(timeoutId);

      // Check if response is ok (status 200-299)
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const message =
          errorData.message ||
          errorData.error ||
          "Chyba pri komunikácii s AI";

        if (response.status === 401 || response.status === 400) {
          throw new Error("Neplatná správa alebo chyba AI");
        } else if (response.status === 404) {
          throw new Error("AI služba nie je dostupná");
        } else if (response.status === 500) {
          throw new Error("Chyba AI servera. Skúste to neskôr.");
        } else {
          throw new Error(message);
        }
      }

      // Parse and return the response data
      const data = await response.json();
      console.log("AI Response data:", data);
      return data;
    } catch (error: any) {
      // Handle different types of errors
      if (error.name === "AbortError") {
        // Request was aborted due to timeout
        throw new Error("AI odpoveď trvala príliš dlho. Skúste to znovu.");
      } else if (
        error.message.includes("Network") ||
        error.message.includes("fetch")
      ) {
        // Network error
        throw new Error(
          "Nemožno sa pripojiť k AI serveru. Skontrolujte internetové pripojenie."
        );
      } else if (error.message) {
        // Custom error message from above
        throw error;
      } else {
        // Other unexpected errors
        throw new Error("Nastala neočakávaná chyba pri komunikácii s AI.");
      }
    }
  };

  /**
   * Handle AI response
   */
  const handleAIResponse = async (userMessage: string) => {
    setIsLoading(true);

    try {
      console.log("Attempting AI chat with message:", userMessage);

      const response = await sendMessageToAI(userMessage);

      console.log("AI chat successful:", response);

      // Extract AI response text from the response
      const aiResponseText = response.response || response.message || "AI odpoveď nie je dostupná";

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: aiResponseText,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiResponse]);

    } catch (error: any) {
      console.error("AI chat failed:", error.message);

      // Show error as AI message
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: `Prepáčte, nastala chyba: ${error.message}`,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorResponse]);
    } finally {
      // Always reset loading state
      setIsLoading(false);
    }
  };

  /**
   * Handle sending a new message
   */
  const handleSendMessage = () => {
    console.log("Environment check:");
    console.log("EXPO_PUBLIC_API_URL:", process.env.EXPO_PUBLIC_API_URL);

    if (inputValue.trim()) {
      const newMessage: Message = {
        id: Date.now().toString(),
        text: inputValue.trim(),
        isUser: true,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, newMessage]);
      const messageText = inputValue.trim();
      setInputValue("");

      // Handle AI response
      handleAIResponse(messageText);
    }
  };

  /**
   * Initialize chat with the prompt if provided
   */
  useEffect(() => {
    if (prompt) {
      const initialMessage: Message = {
        id: Date.now().toString(),
        text: decodeURIComponent(prompt as string),
        isUser: true,
        timestamp: new Date(),
      };
      setMessages([initialMessage]);

      // Send initial prompt to AI after a short delay
      setTimeout(() => {
        handleAIResponse(decodeURIComponent(prompt as string));
      }, 1000);
    }
  }, [prompt]);

  /**
   * Auto-scroll to bottom when new messages are added
   */
  useEffect(() => {
    setTimeout(() => {
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }, 100);
  }, [messages]);

  const goBack = () => {
    router.back();
  };

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      {/* Header */}
      <View className="flex-row items-center px-5 pt-12 pb-4 border-b border-white/10">
        <TouchableOpacity onPress={goBack} className="mr-4">
          <Image
            source={icons.back}
            className="w-6 h-6"
            tintColor="#FFFFFF"
            resizeMode="contain"
          />
        </TouchableOpacity>
        <Text className="text-white text-lg font-semibold flex-1">
          AI Asistent
        </Text>
        {isLoading && (
          <View className="w-2 h-2 bg-green-500 rounded-full" style={{ opacity: 0.8 }} />
        )}
      </View>

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        className="flex-1 px-5"
        contentContainerStyle={{ paddingVertical: 20, paddingBottom: 100 }}
        showsVerticalScrollIndicator={false}
      >
        {messages.map((message) => (
          <View
            key={message.id}
            className={`mb-4 ${message.isUser ? 'items-end' : 'items-start'}`}
          >
            <View
              className={`max-w-[80%] p-4 rounded-2xl ${
                message.isUser
                  ? 'bg-blue-600 rounded-br-md'
                  : 'bg-box border border-stroke rounded-bl-md'
              }`}
              style={!message.isUser ? { borderWidth: 0.5 } : {}}
            >
              <Text className="text-white text-base leading-5">
                {message.text}
              </Text>
              <Text
                className={`text-xs mt-2 ${
                  message.isUser ? 'text-blue-100' : 'text-gray-400'
                }`}
              >
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </Text>
            </View>
          </View>
        ))}

        {/* Loading indicator for AI response */}
        {isLoading && (
          <View className="items-start mb-4">
            <View className="bg-box border border-stroke rounded-2xl rounded-bl-md p-4" style={{ borderWidth: 0.5 }}>
              <Text className="text-white text-base">AI píše...</Text>
            </View>
          </View>
        )}
      </ScrollView>

      {/* Input area */}
      <View className="absolute bottom-5 left-0 right-0 mx-5">
        <KeyboardAwareScrollView
          enableOnAndroid={true}
          keyboardShouldPersistTaps="handled"
          extraScrollHeight={150}
        >
          <View className="bg-accent rounded-lg py-3.5 flex flex-row justify-center items-center">
            <SearchBar
              placeholder={isLoading ? "AI odpoveď..." : "Zadaj svoju správu..."}
              value={inputValue}
              onChangeText={setInputValue}
              onSend={handleSendMessage}
            />
          </View>
        </KeyboardAwareScrollView>
      </View>
    </View>
  );
};

export default Chat;
