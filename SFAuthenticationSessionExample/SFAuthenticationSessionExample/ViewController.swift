//
//  ViewController.swift
//  SFAuthenticationSessionExample
//
//  Created by David Hopkins on 7/14/17.
//  Copyright © 2017 David Hopkins. All rights reserved.
//

import UIKit
import SafariServices

func getQueryStringParameter(url: String, param: String) -> String? {
    guard let url = URLComponents(string: url) else { return nil }
    return url.queryItems?.first(where: { $0.name == param })?.value
}

class ViewController: UIViewController {

    @IBOutlet weak var cookieLabel: UILabel!
    var authSession: SFAuthenticationSession?

    @IBAction func getUserAuth(_ sender: Any) {
        
        let callbackUrl  = "SFAuthenticationSessionExample://"
        let authURL = "http://0.0.0.0:5000/get-cookie/user?callbackUrl=" + callbackUrl
        //Initialize auth session
        self.authSession = SFAuthenticationSession(url: URL(string: authURL)!, callbackURLScheme: callbackUrl, completionHandler: { (callBack:URL?, error:Error? ) in
            guard error == nil, let successURL = callBack else {
                print(error!)
                self.cookieLabel.text = "Error retrieving cookie"
                return
            }
            let user = getQueryStringParameter(url: (successURL.absoluteString), param: "user")
            self.cookieLabel.text = (user == "None") ? "user cookie not set" : "User: " + user!
        })
        cookieLabel.text = "Starting SFAuthenticationSession..."
        self.authSession?.start()
    }
}

