import {
  View,
  Text,
  Image,
  TouchableOpacity,
  TextInput,
  Alert,
  Animated,
  Easing
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
   * Handle button press animation and validation
   */
  const handleSignIn = () => {
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
      Alert.alert("Chyba overenia", "Prosím, vyplňte všetky požadované polia správne.");
      return;
    }

    // TODO: Implement actual authentication logic here
    console.log("Login attempt with:", { userId, password });

    // UNTIL THE LOGIC IS IMPLEMENTED JUST PUT USER INTO THE APP
    router.replace("/(tabs)");
  };

  /**
   * Handle forgot password action
   */
  const handleForgotPassword = () => {
    Alert.alert("Zabudnuté heslo", "Funkcia na obnovenie hesla bude implementovaná.");
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
              textShadowColor: 'rgba(255, 255, 255, 0.3)',
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
                  backgroundColor: 'rgba(107, 114, 128, 0.9)', // More opaque gray
                  borderRadius: 25,
                  borderWidth: 2,
                  borderColor: focusedField === 'userId' ? '#3B82F6' : 'rgba(147, 197, 253, 0.4)', // Light blue border, vibrant when focused
                  shadowColor: focusedField === 'userId' ? '#3B82F6' : 'transparent',
                  shadowOffset: { width: 0, height: 0 },
                  shadowOpacity: 0.3,
                  shadowRadius: 4,
                  elevation: focusedField === 'userId' ? 3 : 0,
                }}
                value={userId}
                onChangeText={setUserId}
                placeholder="Zadajte svoje User ID"
                placeholderTextColor="#ffffff90"
                autoCapitalize="none"
                autoCorrect={false}
                onFocus={() => setFocusedField('userId')}
                onBlur={() => setFocusedField(null)}
              />
            </View>
            {/* Error message for User ID */}
            {errors.userId ? (
              <Text className="text-red-400 text-xs mt-2 text-center">{errors.userId}</Text>
            ) : null}
          </View>

          {/* Enhanced Password input field with icon and focus animation */}
          <View className="mb-10">
            <View className="relative">
              {/* Lock icon inside input */}
              <View className="absolute left-5 top-1/2 transform -translate-y-1/2 z-10">
                <Text className="text-gray-300 text-lg">🔒</Text>
              </View>

              <TextInput
                className="text-white text-base text-center pl-12 pr-6 py-5"
                style={{
                  // Enhanced input styling with more opacity and animated border
                  backgroundColor: 'rgba(107, 114, 128, 0.9)', // More opaque gray
                  borderRadius: 25,
                  borderWidth: 2,
                  borderColor: focusedField === 'password' ? '#3B82F6' : 'rgba(147, 197, 253, 0.4)', // Light blue border, vibrant when focused
                  shadowColor: focusedField === 'password' ? '#3B82F6' : 'transparent',
                  shadowOffset: { width: 0, height: 0 },
                  shadowOpacity: 0.3,
                  shadowRadius: 4,
                  elevation: focusedField === 'password' ? 3 : 0,
                }}
                value={password}
                onChangeText={setPassword}
                placeholder="Zadajte svoje heslo"
                placeholderTextColor="#ffffff90"
                secureTextEntry={true}
                autoCapitalize="none"
                autoCorrect={false}
                onFocus={() => setFocusedField('password')}
                onBlur={() => setFocusedField(null)}
              />
            </View>
            {/* Error message for Password */}
            {errors.password ? (
              <Text className="text-red-400 text-xs mt-2 text-center">{errors.password}</Text>
            ) : null}
          </View>

          {/* Enhanced Sign in button with shadow and press animation */}
          <Animated.View
            style={{
              transform: [{ scale: buttonScaleAnim }],
            }}
          >
            <TouchableOpacity
              className="py-5 px-8"
              style={{
                // Enhanced button styling with shadow and elevation
                backgroundColor: '#2563EB', // Strong blue color
                borderRadius: 25,
                shadowColor: '#000',
                shadowOffset: { width: 0, height: 4 },
                shadowOpacity: 0.3,
                shadowRadius: 6,
                elevation: 8, // Android shadow
              }}
              onPress={handleSignIn}
              activeOpacity={0.8} // Additional touch feedback
            >
              <Text className="text-white text-lg font-semibold text-center">
                Prihlásiť sa
              </Text>
            </TouchableOpacity>
          </Animated.View>

          {/* Forgot password link with extra spacing */}
          <View className="mt-8 items-center">
            <TouchableOpacity onPress={handleForgotPassword}>
              <Text className="text-blue-300 text-sm underline">
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
