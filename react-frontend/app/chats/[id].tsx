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
  const { id, prompt } = useLocalSearchParams<{
    id: string;
    prompt?: string;
  }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollViewRef = useRef<ScrollView>(null);

  /**
   * Get CSRF token from Django
   */
  const getCSRFToken = async () => {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_API_URL}`, {
        method: "GET",
        credentials: "include", // Important for CSRF
      });

      const csrfToken =
        response.headers.get("X-CSRFToken") ||
        response.headers.get("csrftoken") ||
        response.headers.get("csrf-token");

      console.log("CSRF Token from headers:", csrfToken);
      return csrfToken;
    } catch (error) {
      console.log("Failed to get CSRF token:", error);
      return null;
    }
  };

  /**
   * Test if the server is reachable
   */
  const testServerConnectivity = async () => {
    try {
      const baseUrl = process.env.EXPO_PUBLIC_API_URL;
      console.log("Testing server connectivity to:", baseUrl);

      const response = await fetch(baseUrl, {
        method: "GET",
      });

      console.log("Server test response:", response.status);
      return response.status;
    } catch (error) {
      console.log("Server connectivity test failed:", error);
      return null;
    }
  };

  /**
   * Send message to AI backend using the same approach as signin
   */
  const sendMessageToAI = async (userMessage: string) => {
    try {
      const apiUrl = `${process.env.EXPO_PUBLIC_API_URL}chat/response/`;
      console.log("=== AI API DEBUG START ===");
      console.log("Chat API URL:", apiUrl);
      console.log("Environment variable:", process.env.EXPO_PUBLIC_API_URL);
      console.log("Full URL being called:", apiUrl);
      console.log("User message:", userMessage);

      // Create abort controller for timeout functionality
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 36000);

      const requestBody = {
        question: userMessage,
      };

      console.log("Request body:", JSON.stringify(requestBody, null, 2));

      // Prepare headers
      const headers = {
        "Content-Type": "application/json",
      };

      // Add CSRF token to headers if available

      console.log("Request headers:", headers);

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(requestBody),
        signal: controller.signal,
        credentials: "include", // Important for CSRF
      });

      console.log("=== RESPONSE RECEIVED ===");
      console.log("Response status:", response.status);
      console.log("Response statusText:", response.statusText);
      console.log("Response URL:", response.url);

      // Log response headers
      const responseHeaders = {};
      response.headers.forEach((value, key) => {
        responseHeaders[key] = value;
      });
      console.log("Response headers:", responseHeaders);

      clearTimeout(timeoutId);

      // Get the raw response text for debugging
      const responseText = await response.text();
      console.log("Raw response text:", responseText);
      console.log("Response text length:", responseText.length);

      if (!response.ok) {
        console.log("=== ERROR RESPONSE DETAILS ===");
        console.log("Status:", response.status);
        console.log("Status Text:", response.statusText);
        console.log("Raw Response:", responseText);

        let errorData = {};
        try {
          errorData = responseText ? JSON.parse(responseText) : {};
          console.log("Parsed error data:", errorData);
        } catch (parseError) {
          console.log("Failed to parse error response as JSON:", parseError);
          errorData = { message: responseText || "Unknown error" };
        }

        const message =
          errorData.message ||
          errorData.error ||
          errorData.detail ||
          "Chyba pri komunikácii s AI";

        if (response.status === 403) {
          throw new Error(
            `CSRF Error (403): Skúste reštartovať aplikáciu. ${message}`
          );
        } else if (response.status === 401 || response.status === 400) {
          throw new Error(
            `Neplatná správa alebo chyba AI (${response.status}): ${message}`
          );
        } else if (response.status === 404) {
          throw new Error(
            `AI služba nie je dostupná (404): Endpoint ${apiUrl} neexistuje`
          );
        } else if (response.status === 405) {
          throw new Error(
            `Method not allowed (405): POST nie je povolené pre ${apiUrl}`
          );
        } else if (response.status === 500) {
          throw new Error(`Chyba AI servera (500): ${message}`);
        } else if (response.status === 502 || response.status === 503) {
          throw new Error(`Server nedostupný (${response.status}): ${message}`);
        } else {
          throw new Error(`HTTP Error ${response.status}: ${message}`);
        }
      }

      // Parse successful response
      let data;
      try {
        data = responseText ? JSON.parse(responseText) : {};
        console.log("=== SUCCESS RESPONSE ===");
        console.log("Parsed data:", data);
      } catch (parseError) {
        console.log("=== JSON PARSE ERROR ===");
        console.log("Parse error:", parseError);
        console.log("Trying to parse:", responseText);
        throw new Error("Invalid JSON response from server");
      }

      return data;
    } catch (error: any) {
      console.log("=== CATCH BLOCK ERROR ===");
      console.log("Error name:", error.name);
      console.log("Error message:", error.message);
      console.log("Error stack:", error.stack);
      console.log("Full error object:", error);

      if (error.name === "AbortError") {
        throw new Error("AI odpoveď trvala príliš dlho. Skúste to znovu.");
      } else if (
        error.message.includes("Network") ||
        error.message.includes("fetch") ||
        error.message.includes("Failed to fetch") ||
        error.name === "TypeError"
      ) {
        throw new Error(
          `Nemožno sa pripojiť k serveru: ${process.env.EXPO_PUBLIC_API_URL}. Skontrolujte pripojenie a server.`
        );
      } else if (error.message) {
        throw error;
      } else {
        throw new Error("Nastala neočakávaná chyba pri komunikácii s AI.");
      }
    }
  };

  /**
   * Handle AI response with enhanced debugging
   */
  const handleAIResponse = async (userMessage: string) => {
    setIsLoading(true);

    try {
      console.log("=== STARTING AI RESPONSE ===");
      console.log("User message:", userMessage);
      console.log("Environment URL:", process.env.EXPO_PUBLIC_API_URL);

      // Test server connectivity first
      const serverStatus = await testServerConnectivity();
      console.log("Server connectivity test result:", serverStatus);

      const response = await sendMessageToAI(userMessage);
      console.log("AI chat successful:", response);

      const aiResponseText =
        response.response || response.message || "AI odpoveď nie je dostupná";

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: aiResponseText,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiResponse]);
    } catch (error: any) {
      console.error("=== AI CHAT FAILED ===");
      console.error("Error message:", error.message);
      console.error("Full error:", error);

      // Show detailed error for debugging
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: `Debug Error: ${error.message}\n\nAPI URL: ${process.env.EXPO_PUBLIC_API_URL}chat/response/\n\nCheck console for detailed logs.`,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorResponse]);
    } finally {
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

      setMessages((prev) => [...prev, newMessage]);
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
      handleAIResponse(decodeURIComponent(prompt as string));
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
          <View
            className="w-2 h-2 bg-green-500 rounded-full"
            style={{ opacity: 0.8 }}
          />
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
            className={`mb-4 ${message.isUser ? "items-end" : "items-start"}`}
          >
            <View
              className={`max-w-[80%] p-4 rounded-2xl ${
                message.isUser
                  ? "bg-blue-600 rounded-br-md"
                  : "bg-box border border-stroke rounded-bl-md"
              }`}
              style={!message.isUser ? { borderWidth: 0.5 } : {}}
            >
              <Text className="text-white text-base leading-5">
                {message.text}
              </Text>
              <Text
                className={`text-xs mt-2 ${
                  message.isUser ? "text-blue-100" : "text-gray-400"
                }`}
              >
                {message.timestamp.toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </Text>
            </View>
          </View>
        ))}

        {/* Loading indicator for AI response */}
        {isLoading && (
          <View className="items-start mb-4">
            <View
              className="bg-box border border-stroke rounded-2xl rounded-bl-md p-4"
              style={{ borderWidth: 0.5 }}
            >
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
              placeholder={
                isLoading ? "AI odpoveď..." : "Zadaj svoju správu..."
              }
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
