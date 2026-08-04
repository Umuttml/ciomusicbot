exports.success = (res, data = {}, message = "Başarılı") => {
    return res.status(200).json({
        success: true,
        message,
        data
    });
};

exports.error = (res, status = 500, message = "Sunucu hatası") => {
    return res.status(status).json({
        success: false,
        message
    });
};