import { createContext } from "react";

const UrlContext = createContext({
  backendUrl: "",
  websocketUrl: "",
  websiteProtocol: "",
  websiteAddress: "",
});

export default UrlContext;
