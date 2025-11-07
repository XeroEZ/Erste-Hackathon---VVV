import {
  View,
  Text,
  Image,
  TouchableOpacity,
  TextInput,
  Alert,
  Animated,
  Easing,
  ActivityIndicator,
} from "react-native";
import React, { useState, useRef, useEffect } from "react";
import { images } from "@/constants/images";
import { router } from "expo-router";

const signin = () => {
  // State management for form inputs
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({ userId: "", password: "" });
  const [focusedField, setFocusedField] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false); // Loading state for API call
  const [showPassword, setShowPassword] = useState(false); // State for password visibility

  // Animation refs for fade-in effects
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const titleAnim = useRef(new Animated.Value(0)).current;
  const inputsAnim = useRef(new Animated.Value(0)).current;

  // Animation ref for button press feedback
  const buttonScaleAnim = useRef(new Animated.Value(1)).current;

  /**
   * Initialize fade-in animations on component mount
   */
  useEffect(() => {
    // Stagger the animations for a smooth entrance effect
    Animated.sequence([
      // Title animation
      Animated.timing(titleAnim, {
        toValue: 1,
        duration: 800,
        easing: Easing.out(Easing.quad),
        useNativeDriver: true,
      }),
      // Input fields animation (slightly delayed)
      Animated.timing(inputsAnim, {
        toValue: 1,
        duration: 600,
        easing: Easing.out(Easing.quad),
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  /**
   * Validate form inputs before submission
   * Returns true if all validations pass, false otherwise
   */
  const validateInputs = () => {
    const newErrors = { userId: "", password: "" };
    let isValid = true;

    // Check if User ID is empty
    if (!userId.trim()) {
      newErrors.userId = "User ID je povinné";
      isValid = false;
    }

    // Check if password is empty
    if (!password.trim()) {
      newErrors.password = "Heslo je povinné";
      isValid = false;
    } else if (password.length < 6) {
      // Optional: Add minimum password length validation
      newErrors.password = "Heslo musí mať aspoň 6 znakov";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  /**
   * Send login request to backend API using native fetch
   */
  const authenticateUser = async (username: string, password: string) => {
    try {
      // Create abort controller for timeout functionality
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

      const response = await fetch("http://localhost:8000/api/banking/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
        signal: controller.signal, // For timeout functionality
      });

      // Clear the timeout since request completed
      clearTimeout(timeoutId);

      // Check if response is ok (status 200-299)
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const message =
          errorData.message ||
          errorData.error ||
          "Neplatné prihlasovacie údaje";

        if (response.status === 401 || response.status === 400) {
          throw new Error("Nesprávne používateľské meno alebo heslo");
        } else if (response.status === 500) {
          throw new Error("Chyba servera. Skúste to neskôr.");
        } else {
          throw new Error(message);
        }
      }

      // Parse and return the response data
      const data = await response.json();
      return data;
    } catch (error: any) {
      // Handle different types of errors
      if (error.name === "AbortError") {
        // Request was aborted due to timeout
        throw new Error("Požiadavka trvala príliš dlho. Skúste to znovu.");
      } else if (
        error.message.includes("Network") ||
        error.message.includes("fetch")
      ) {
        // Network error
        throw new Error(
          "Nemožno sa pripojiť k serveru. Skontrolujte internetové pripojenie."
        );
      } else if (error.message) {
        // Custom error message from above
        throw error;
      } else {
        // Other unexpected errors
        throw new Error("Nastala neočakávaná chyba. Skúste to znovu.");
      }
    }
  };

  /**
   * Handle button press animation, validation, and API call
   */
  const handleSignIn = async () => {
    // Button press animation - scale down then back up
    Animated.sequence([
      Animated.timing(buttonScaleAnim, {
        toValue: 0.95,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(buttonScaleAnim, {
        toValue: 1,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();

    // Clear previous errors
    setErrors({ userId: "", password: "" });

    // Validate inputs
    if (!validateInputs()) {
      Alert.alert(
        "Chyba overenia",
        "Prosím, vyplňte všetky požadované polia správne."
      );
      return;
    }

    // Set loading state
    setIsLoading(true);

    try {
      // Call backend API for authentication using fetch
      console.log("Attempting login with:", {
        username: userId,
        password: password,
      });

      const response = await authenticateUser(userId, password);

      console.log("Login successful:", response);

      // TODO: Store authentication token if provided by backend
      // const token = response.token;
      // await AsyncStorage.setItem('authToken', token);

      // Navigate to main app on successful authentication
      router.replace("/(tabs)");
    } catch (error: any) {
      console.error("Login failed:", error.message);

      // Show error message to user
      Alert.alert("Prihlásenie neúspešné", error.message, [{ text: "OK" }]);
    } finally {
      // Always reset loading state
      setIsLoading(false);
    }
    router.replace("/(tabs)");
  };

  /**
   * Handle forgot password action
   */
  const handleForgotPassword = () => {
    Alert.alert(
      "Zabudnuté heslo",
      "Funkcia na obnovenie hesla bude implementovaná."
    );
  };

  /**
   * Toggle password visibility
   */
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <View className="flex-1 bg-black">
      {/* Background image */}
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      {/* Center the content */}
      <View className="flex-1 justify-center items-center px-8">
        {/* Enhanced title with shadow/glow effect and fade-in animation */}
        <Animated.View
          style={{
            opacity: titleAnim,
            transform: [
              {
                translateY: titleAnim.interpolate({
                  inputRange: [0, 1],
                  outputRange: [-20, 0],
                }),
              },
            ],
          }}
        >
          <Text
            className="text-white text-4xl font-bold text-center mb-20"
            style={{
              // Enhanced title styling with shadow/glow
              textShadowColor: "rgba(255, 255, 255, 0.3)",
              textShadowOffset: { width: 0, height: 0 },
              textShadowRadius: 8,
              elevation: 5,
            }}
          >
            Prihlásenie
          </Text>
        </Animated.View>

        {/* Login form container with fade-in animation */}
        <Animated.View
          className="w-full mb-8"
          style={{
            opacity: inputsAnim,
            transform: [
              {
                translateY: inputsAnim.interpolate({
                  inputRange: [0, 1],
                  outputRange: [30, 0],
                }),
              },
            ],
          }}
        >
          {/* Enhanced User ID input field with icon and focus animation */}
          <View className="mb-6">
            <View className="relative">
              {/* User icon inside input */}
              <View className="absolute left-5 top-1/2 transform -translate-y-1/2 z-10">
                <Text className="text-gray-300 text-lg">👤</Text>
              </View>

              <TextInput
                className="text-white text-base text-center pl-12 pr-6 py-5"
                style={{
                  // Enhanced input styling with more opacity and animated border
                  backgroundColor: "rgba(107, 114, 128, 0.9)", // More opaque gray
                  borderRadius: 25,
                  borderWidth: 2,
                  borderColor:
                    focusedField === "userId"
                      ? "#3B82F6"
                      : "rgba(147, 197, 253, 0.4)", // Light blue border, vibrant when focused
                  shadowColor:
                    focusedField === "userId" ? "#3B82F6" : "transparent",
                  shadowOffset: { width: 0, height: 0 },
                  shadowOpacity: 0.3,
                  shadowRadius: 4,
                  elevation: focusedField === "userId" ? 3 : 0,
                }}
                value={userId}
                onChangeText={setUserId}
                placeholder="Zadajte svoje User ID"
                placeholderTextColor="#ffffff90"
                autoCapitalize="none"
                autoCorrect={false}
                editable={!isLoading} // Disable input when loading
                onFocus={() => setFocusedField("userId")}
                onBlur={() => setFocusedField(null)}
              />
            </View>
            {/* Error message for User ID */}
            {errors.userId ? (
              <Text className="text-red-400 text-xs mt-2 text-center">
                {errors.userId}
              </Text>
            ) : null}
          </View>

          {/* Enhanced Password input field with icon, eye toggle, and focus animation */}
          <View className="mb-10">
            <View className="relative">
              {/* Lock icon inside input */}
              <View className="absolute left-5 top-1/2 transform -translate-y-1/2 z-10">
                <Text className="text-gray-300 text-lg">🔒</Text>
              </View>

              {/* Password visibility toggle button */}
              <TouchableOpacity
                className="absolute right-5 top-1/2 transform -translate-y-1/2 z-10"
                onPress={togglePasswordVisibility}
                disabled={isLoading}
              >
                <Text className="text-gray-300 text-lg">
                  {showPassword ? "👁️" : "👁️‍🗨️"}
                </Text>
              </TouchableOpacity>

              <TextInput
                className="text-white text-base text-center pl-12 pr-12 py-5"
                style={{
                  // Enhanced input styling with more opacity and animated border
                  backgroundColor: "rgba(107, 114, 128, 0.9)", // More opaque gray
                  borderRadius: 25,
                  borderWidth: 2,
                  borderColor:
                    focusedField === "password"
                      ? "#3B82F6"
                      : "rgba(147, 197, 253, 0.4)", // Light blue border, vibrant when focused
                  shadowColor:
                    focusedField === "password" ? "#3B82F6" : "transparent",
                  shadowOffset: { width: 0, height: 0 },
                  shadowOpacity: 0.3,
                  shadowRadius: 4,
                  elevation: focusedField === "password" ? 3 : 0,
                }}
                value={password}
                onChangeText={setPassword}
                placeholder="Zadajte svoje heslo"
                placeholderTextColor="#ffffff90"
                secureTextEntry={!showPassword} // Toggle based on showPassword state
                autoCapitalize="none"
                autoCorrect={false}
                editable={!isLoading} // Disable input when loading
                onFocus={() => setFocusedField("password")}
                onBlur={() => setFocusedField(null)}
              />
            </View>
            {/* Error message for Password */}
            {errors.password ? (
              <Text className="text-red-400 text-xs mt-2 text-center">
                {errors.password}
              </Text>
            ) : null}
          </View>

          {/* Enhanced Sign in button with shadow, press animation, and loading state */}
          <Animated.View
            style={{
              transform: [{ scale: buttonScaleAnim }],
            }}
          >
            <TouchableOpacity
              className="py-5 px-8"
              style={{
                // Enhanced button styling with shadow and elevation
                backgroundColor: isLoading ? "#94A3B8" : "#2563EB", // Gray when loading, blue when ready
                borderRadius: 25,
                shadowColor: "#000",
                shadowOffset: { width: 0, height: 4 },
                shadowOpacity: 0.3,
                shadowRadius: 6,
                elevation: 8, // Android shadow
              }}
              onPress={handleSignIn}
              disabled={isLoading} // Disable button when loading
              activeOpacity={0.8} // Additional touch feedback
            >
              {isLoading ? (
                // Show loading spinner when API call is in progress
                <View className="flex-row justify-center items-center">
                  <ActivityIndicator color="white" size="small" />
                  <Text className="text-white text-lg font-semibold ml-2">
                    Prihlasuje sa...
                  </Text>
                </View>
              ) : (
                <Text className="text-white text-lg font-semibold text-center">
                  Prihlásiť sa
                </Text>
              )}
            </TouchableOpacity>
          </Animated.View>

          {/* Forgot password link with extra spacing */}
          <View className="mt-8 items-center">
            <TouchableOpacity
              onPress={handleForgotPassword}
              disabled={isLoading}
            >
              <Text
                className={`text-sm underline ${
                  isLoading ? "text-gray-500" : "text-blue-300"
                }`}
              >
                Zabudli ste heslo?
              </Text>
            </TouchableOpacity>
          </View>
        </Animated.View>
      </View>
    </View>
  );
};

export default signin;
